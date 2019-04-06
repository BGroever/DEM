/*
CS205 project:    Density equalizing map projections
Date:             April 6th 2019

Compiler:         gcc diff_map2.c -o exec -lm -lpng
project members:  Millie Zhou, Lemaire Baptiste, Benedikt Groever
project goal:     density equalizing map projections
Input files:      -colchart.txt
                  -density.txt
                  -usa_vs.png
Output file:      -dens_eq.png
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <png.h>
#include <math.h>
#define SIZE 50

/* helper functions (which are not needed in python prototype version) */

//Find index of string na in string array c
static int getStringIndex(char (*c)[256], char *na)
{
    for(int j=0; j < SIZE; j++){
        if(strcmp(na,c[j]) == 0){
          return j;
        }
    }
}

//Find index of el in int array c
static int getIntIndex(int *c, int  el)
{
    for(int j=0; j < SIZE; j++){
        if(el == c[j]){
          return j;
        }
    }
    return -1;
}

// PNG image parameters
int width, height;
png_byte color_type;
png_byte bit_depth;
png_bytep *row_pointers;

//Reader of png file
void read_png_file(char *filename)
{
    FILE *fp = fopen(filename, "rb");

    png_structp png = png_create_read_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);
    if(!png) abort();

    png_infop info = png_create_info_struct(png);
    if(!info) abort();

    if(setjmp(png_jmpbuf(png))) abort();

    png_init_io(png, fp);

    png_read_info(png, info);

    width      = png_get_image_width(png, info);
    height     = png_get_image_height(png, info);
    color_type = png_get_color_type(png, info);
    bit_depth  = png_get_bit_depth(png, info);

    // Read any color_type into 8bit depth, RGBA format.
    // See http://www.libpng.org/pub/png/libpng-manual.txt

    if(bit_depth == 16)
      png_set_strip_16(png);

    if(color_type == PNG_COLOR_TYPE_PALETTE)
      png_set_palette_to_rgb(png);

    // PNG_COLOR_TYPE_GRAY_ALPHA is always 8 or 16bit depth.
    if(color_type == PNG_COLOR_TYPE_GRAY && bit_depth < 8)
      png_set_expand_gray_1_2_4_to_8(png);

    if(png_get_valid(png, info, PNG_INFO_tRNS))
      png_set_tRNS_to_alpha(png);

    // These color_type don't have an alpha channel then fill it with 0xff.
    if(color_type == PNG_COLOR_TYPE_RGB ||
       color_type == PNG_COLOR_TYPE_GRAY ||
       color_type == PNG_COLOR_TYPE_PALETTE)
      png_set_filler(png, 0xFF, PNG_FILLER_AFTER);

    if(color_type == PNG_COLOR_TYPE_GRAY ||
       color_type == PNG_COLOR_TYPE_GRAY_ALPHA)
      png_set_gray_to_rgb(png);

    png_read_update_info(png, info);

    row_pointers = (png_bytep*)malloc(sizeof(png_bytep) * height);
    for(int y = 0; y < height; y++) {
      row_pointers[y] = (png_byte*)malloc(png_get_rowbytes(png,info));
    }

    png_read_image(png, row_pointers);

    fclose(fp);
}

//Writer of png file
void write_png_file(char *filename)
{
    int y;

    FILE *fp = fopen(filename, "wb");
    if(!fp) abort();

    png_structp png = png_create_write_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);
    if (!png) abort();

    png_infop info = png_create_info_struct(png);
    if (!info) abort();

    if (setjmp(png_jmpbuf(png))) abort();

    png_init_io(png, fp);

    // Output is 8bit depth, RGBA format.
    png_set_IHDR(
      png,
      info,
      width, height,
      8,
      PNG_COLOR_TYPE_RGBA,
      PNG_INTERLACE_NONE,
      PNG_COMPRESSION_TYPE_DEFAULT,
      PNG_FILTER_TYPE_DEFAULT
    );
    png_write_info(png, info);

    // To remove the alpha channel for PNG_COLOR_TYPE_RGB format,
    // Use png_set_filler().
    // png_set_filler(png, 0, PNG_FILLER_AFTER);

    png_write_image(png, row_pointers);
    png_write_end(png, NULL);

    for(int y = 0; y < height; y++) {
      free(row_pointers[y]);
    }
    free(row_pointers);

    fclose(fp);
}

// main program for density equalizing map projections
int main(void)
{
    /* Read in the color values for each state */
    char const* const fileName = "colchart.txt";
    FILE* file = fopen(fileName, "r");
    char line[256];
    int d[SIZE] = {0};
    char c[SIZE][256] = {{'\0'}};
    int k=0;

    while (fgets(line, sizeof(line), file)) {
        char *token = strtok(strtok(line,"\n"), " ");
        int i = 0;
        char a[5][256] = {{'\0'},{'\0'},{'\0'},{'\0'},{'\0'}};
        while (token != NULL)
        {
            strcpy(a[i], token);
            token = strtok(NULL, " ");
            i = i + 1;
        }

        /* Read in the three color channels */
        int re = atoi(a[0]);
        int gr = atoi(a[1]);
        int bl = atoi(a[2]);

        /* Read in the name of the state, taking care to handle to
        states space in them */
        char na[256];
        if(*a[4]=='\0'){
            strcpy(na, a[3]);
        }else{
            strcpy(na, a[3]);
            strcat(na, " ");
            strcat(na, a[4]);
        }
        strcpy(c[k], na);

        /* Encode the color into a single integer, and store the information */
        int nu = re+256*gr+65536*bl;
        d[k] = nu;
        k+=1;
    }

    fclose(file);

    /* Read in the population densities for each state */
    char const* const fileName2 = "density.txt";
    FILE* file2 = fopen(fileName2, "r");
    double rh[SIZE] = {0};

    while (fgets(line, sizeof(line), file2)) {

        char *token = strtok(strtok(line,"\n"), " ");
        int i = 0;
        char a[3][256] = {{'\0'},{'\0'},{'\0'}};

        while (token != NULL)
        {
            strcpy(a[i], token);
            token = strtok(NULL, " ");
            i = i + 1;
        }

        char na[256];
        if(*a[2]=='\0'){
            strcpy(na, a[1]);
        }else{
            strcpy(na, a[1]);
            strcat(na, " ");
            strcat(na, a[2]);
        }
        int m = getStringIndex(c, na);
        rh[m] = atoll(a[0]);
    }

    /* TESTING
    c  - string array for the name of the states
    d  - unique bar code for each state (RGB) = R+256*G+65536*B
    rh[k] - population density of state c[k] */
    for(int j=0; j<SIZE; j++){
      printf("%s, %d, %f\n", c[j], d[j], rh[j]);
    }

    /* Read in the undeformed US map */
    read_png_file("usa_vs.png");
    int z = 3;

    int o[width][height][z];
    for(int y = 0; y < height; y++) {
      png_bytep row = row_pointers[y];
      for(int x = 0; x < width; x++) {
        png_bytep px = &(row[x * 4]);
        //printf("%d, %d, %d\n", px[0], px[1], px[2]);
        for(int l = 0; l < z; l++){
          o[x][y][l] = px[l];
        }
      }
    }

    /* Grid spacing */
    double h   = 1.0;
    double ih2 = 0.5/h;

    /* Scan the image to set the density field in the states.
    In addition, calculate the average density. */
    double u[width][height];
    double cu[width][height];
    double srho = 0.0;
    int npts = 0;
    int co;
    int index;

    for(int y=0; y < height; y++){
      for(int x=0; x < width; x++){
        co = o[x][y][0]+256*o[x][y][1]+65536*o[x][y][2];
        index = getIntIndex(d, co);
        if (index != -1){
          u[x][y] = rh[index];
          srho+=u[x][y];
          npts+=1;
        }
        else if(co != 16777215){
          abort();
        }
      }
    }

    /* Re-scan over the image to set the average density
    in regions outside the states */
    double rhobar=srho/npts;
    printf("Avg. rho: %f\n", rhobar);
    for(int y=0; y < height; y++){
      for(int x=0; x < width; x++){
        co = o[x][y][0]+256*o[x][y][1]+65536*o[x][y][2];
        if(co==16777215){
          u[x][y] = rhobar;
        }
      }
    }

    /* Initialize the reference map coordinates */
    double X[width][height][2];
    double cX[width][height][2];
    for(int y=0; y < height; y++){
      for(int x=0; x < width; x++){
        X[x][y][0] = h*x;
        X[x][y][1] = h*y;
      }
    }

    /* Calculate timestep size */
    double dt = 0.24*h*h;
    double T  = (height*height+width*width)/12.0;
    int nsteps = (int) ceil(T/dt);
    dt = T/nsteps;
    printf("Solving to T= %10f using %d timesteps.\n", T, nsteps);

    /* Function to integrate the density and reference
    map fields forward in time by dt */
    void step(double dt){

      /* Calculate the upwinded update for the reference map */

      /* Do the finite-difference update */

      /* Print the current time and the extremal values of density */

    }

    /* Perform the integration timesteps, using the smaller
    dt for the first few steps to deal with the large velocities
    that initially occur */
    double time = 0;
    for(int l=0; l < 24; l++){
      step(dt/24.0);
    }

    /* You need to implement the larger time steps too (Python code line
    145-146), I would do this at the very end since they take a long time
    to run  */



    /* Use the deformed reference map to plot the density-equalized US map */
    int o2[width][height][z];
    memset(o2, 255, sizeof(o2)); //This initializes o2 to 255.

    // Set the values of o2 through conversion of Python code lines 150 - 158

    for(int y = 0; y < height; y++) {
      png_bytep row = row_pointers[y];
      for(int x = 0; x < width; x++) {
        png_bytep px = &(row[x * 4]);
        for(int l = 0; l < z; l++){
          px[l] = o2[x][y][l];
        }
      }
    }

    write_png_file("dens_eq.png");

    return 0;

}
