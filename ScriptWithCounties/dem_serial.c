/*
CS205 project:    Density equalizing map projections
Date:             April 6th 2019

Compiler:         gcc diff_map2.c -o exec -lm -lpng
project members:  Millie Zhou, Baptiste Lemaire, Benedikt Groever
project goal:     density equalizing map projections
Input files:      -colchart_counties.txt
                  -den_per_county.txt
                  -uscounties.png
Output file:      -dens_eq.png
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <png.h>
#include <math.h>
#include <omp.h>

// Number of states/entities to calculates:
#define SIZE 3142

/** helper functions (which are not needed in python prototype version). */

/** Finds the index of string na in string array c. */
static int getStringIndex(int* c, int na)
{
    for(int j=0; j < SIZE; j++){
        if(c[j] == na){
          return j;
        }
    }
    return 0;
}

/** Finds index of el in int array c. */
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
int width, height, size_img;
png_byte color_type;
png_byte bit_depth;
png_bytep *row_pointers;

/** Reader of png file. */
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
    size_img   = width * height;
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

/** Writer of png file. */
void write_png_file(char *filename)
{
    // int y;

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

/** Function to integrate the density and reference
  * map fields forward in time by dt. */

void step(double dt, double *time, double *u, double *cu, double *X, double *cX, double h, double ih2) {

    double nu = dt/(h*h);
    double fac = ih2*dt/h;
    double vx = 0;
    double vy = 0;

    // Calculate the upwinded update for the reference map.
    for(int i=0; i < height; i++){
      for(int j=0; j < width; j++){

        if ((i>0) && (i<height-1)) {
          vx = (-1.0) * (u[(i+1)*width+j]-u[(i-1)*width+j]) * fac / u[i*width+j];
          if (vx > 0) {
            cX[i*width*2+j*2+0] = vx*(-1*X[i*width*2+j*2+0] + X[(i-1)*width*2+j*2+0]);
            cX[i*width*2+j*2+1] = vx*(-1*X[i*width*2+j*2+1] + X[(i-1)*width*2+j*2+1]);
          }else{
            cX[i*width*2+j*2+0] = vx*(   X[i*width*2+j*2+0] - X[(i+1)*width*2+j*2+0]);
            cX[i*width*2+j*2+1] = vx*(   X[i*width*2+j*2+1] - X[(i+1)*width*2+j*2+1]);
          }
        }else{
            cX[i*width*2+j*2+0] = 0.0;
            cX[i*width*2+j*2+1] = 0.0;
        }


        if ( (j>0) && (j<width-1)) {
          vy = (-1.0) * (u[i*width+(j+1)]-u[i*width+(j-1)]) * fac / u[i*width+j];
          if (vy > 0) {
            cX[i*width*2+j*2+0] += vy*(-1*X[i*width*2+j*2+0]+X[i*width*2+(j-1)*2+0]);
            cX[i*width*2+j*2+1] += vy*(-1*X[i*width*2+j*2+1]+X[i*width*2+(j-1)*2+1]);
          } else {
            cX[i*width*2+j*2+0] += vy*(X[i*width*2+j*2+0]-1*X[i*width*2+(j+1)*2+0]);
            cX[i*width*2+j*2+1] += vy*(X[i*width*2+j*2+1]-1*X[i*width*2+(j+1)*2+1]);
          }
        }
      }
    }
    for(int i=0; i < height; i++){
      for(int j=0; j < width; j++){
        X[i*width*2+j*2+0] += cX[i*width*2+j*2+0];
        X[i*width*2+j*2+1] += cX[i*width*2+j*2+1];
      }
    }

    //int i = 50;
    //int j = 150;
    //vx = (-1.0) * (u[(i+1)*width+j]-u[(i-1)*width+j]) * fac / u[i*width+j];
    //vy = (-1.0) * (u[i*width+(j+1)]-u[i*width+(j-1)]) * fac / u[i*width+j];
    //printf("vx: %e for %d, vy: %e for %d\n", vx, i, vy, j);
    //printf("x:  %e, y: %e\n", cX[i*width*2+j*2+0], cX[i*width*2+j*2+1]);

    // Does the finite-difference update
    double tem;
    int k;
    for (int i=0; i<height; i++) {
        for (int j=0; j<width; j++) {
            if (i>0){
                tem = u[(i-1)*width+j]; k = 1;
            }else{
                tem = 0; k = 0;
            }
            if (j>0){
                tem += u[i*width+(j-1)]; k += 1;
            }
            if (j<width-1){
                tem += u[i*width+(j+1)]; k += 1;
            }
            if (i<height-1){
                tem += u[(i+1)*width+j]; k += 1;
            }
            cu[i*width+j] = tem - k * u[i*width+j];
        }
    }
    #pragma omp parallel for schedule(static)
    for (int i=0; i<size_img; i++){
      u[i] += cu[i] * nu;
    }
    
    /*
    for(int i=0; i < height; i++){
      for(int j=0; j < width; j++){
        u[i*width+j] += cu[i*width+j] * nu;
      }
    }
    */

    // Prints the current time and the extremal values of density.
    *time += dt;
    double minU=16777215;
    for (int i=0; i<size_img; i++){
      minU = minU < u[i] ? minU : u[i];
    }

    /*for (int i=0; i<height; i++) {
      for (int j=0; j<width; j++) {
        if (u[i*width+j] < minU) {
          minU = u[i*width+j];
        }
      }
    }
    */

    double maxU=0.0;
    for (int i=0; i<size_img; i++){
      maxU = maxU > u[i] ? maxU : u[i];
    }
    /*
    for (int i=0; i<height; i++) {
      for (int j=0; j<width; j++) {
        if (u[i*width+j] > maxU) {
          maxU = u[i*width+j];
        }
      }
    }
    */

    printf("%f, %f, %f \n", *time, minU, maxU);
}

/** Main program for density equalizing map projections. */
int main(void)
{
    // timing_t tstart, tend; 
    //timing_t tstart, tend;
    //get_time(&tstart);
    double tstart=omp_get_wtime(), tend;

    // Read in the color values for each state. 
    char const* const fileName = "colchart_counties.txt";
    FILE* file = fopen(fileName, "r");
    char line[256];
    int d[SIZE] = {0};
    //char c[SIZE][256] = {{'\0'}};
    int c[SIZE] = {0};
    int k=0;

    while (fgets(line, sizeof(line), file)) {
        char *token = strtok(strtok(line,"\n"), " ");
        int i = 0;
        char a[4][256] = {{'\0'},{'\0'},{'\0'},{'\0'}};
        while (token != NULL)
        {
            strcpy(a[i], token);
            token = strtok(NULL, " ");
            i = i + 1;
        }

        // Read in the three color channels. 
        int re = atoi(a[0]);
        int gr = atoi(a[1]);
        int bl = atoi(a[2]);
        int na = atoi(a[3]);
        c[k]=na;

        // Read in the name of the state, taking care to handle to
        // states space in them.
        //char na[256];
        //if(*a[4]=='\0'){
        //    strcpy(na, a[3]);
        //}else{
        //    strcpy(na, a[3]);
        //    strcat(na, " ");
        //    strcat(na, a[4]);
        //}
        //strcpy(c[k], na);

        // Encode the color into a single integer, and store the information.
        int nu = re+256*gr+65536*bl;
        d[k] = nu;
        k+=1;
    }

    fclose(file);

    // Read in the population densities for each state.
    char const* const fileName2 = "den_per_county.txt";
    FILE* file2 = fopen(fileName2, "r");
    double rh[SIZE] = {0};

    while (fgets(line, sizeof(line), file2)) {

        char *token = strtok(strtok(line,"\n"), "\t");
        int i = 0;
        char a[3][256] = {{'\0'},{'\0'},{'\0'}};

        while (token != NULL)
        {
            strcpy(a[i], token);
            token = strtok(NULL, " ");
            i = i + 1;
        }
        int na = atoll(a[1]);
        //char na[256];
        //if(*a[2]=='\0'){
        //    strcpy(na, a[1]);
        //}else{
        //    strcpy(na, a[1]);
        //    strcat(na, " ");
        //    strcat(na, a[2]);
        //}
        int m = getStringIndex(c, na);
        rh[m] = atof(a[0]);
        if (rh[m]==0) printf("Density of 0.0 for fips=%d\n",na);
    }

    // TESTING
    //  c  - string array for the name of the states
    //  d  - unique bar code for each state (RGB) = R+256*G+65536*B
    //  rh[k] - population density of state c[k].
    //
    //  for(int j=0; j<SIZE; j++){
    //  printf("%s, %d, %f\n", c[j], d[j], rh[j]);
    //}

    // Reads in the undeformed US map.
    read_png_file("uscounties.png");
    //get_time(&tend);
    tend = omp_get_wtime();
    printf("Elapsed time load data: %f s\n", tend-tstart); //timespec_diff(tstart, tend));

    //get_time(&tstart);
    tstart = omp_get_wtime();

    int z = 3;
    int *o = malloc(height*width*z * sizeof(int));
    for(int i = 0; i < height; i++) {
      png_bytep row = row_pointers[i];
      for(int j = 0; j < width; j++) {
        png_bytep py = &(row[j * 4]);
        o[i*width*z+j*z+0] = py[0];
        o[i*width*z+j*z+1] = py[1];
        o[i*width*z+j*z+2] = py[2];
      }
    }
    // Grid spacing.
    double h   = 1.0;
    double ih2 = 0.5/h;

    // Scan the image to set the density field in the states.
    // In addition, calculate the average density. */
    double *u = malloc(height*width * sizeof(double));
    double *cu = malloc(height*width * sizeof(double));
    double srho = 0.0;
    int npts = 0;
    int co;
    int index;

    for(int i=0; i < height; i++){
      for(int j=0; j < width; j++){
        co = o[i*width*z+j*z+0]+256*o[i*width*z+j*z+1]+65536*o[i*width*z+j*z+2];
        index = getIntIndex(d, co);
        if (index != -1){
          u[i*width+j] = rh[index];
          srho+=u[i*width+j];
          npts+=1;
        }
        else if(co != 16777215){
          printf("Mayday Mayday, we are aborting! Index=%d and Co=%d\n",index,co);
          printf("i=%d\tj=%d\n",i,j);
          abort();
        }
      }
    }

    // Re-scan over the image to set the average density
    // in regions outside the states.
    double rhobar=srho/npts;
    printf("Avg. rho: %f\n", rhobar);
    for(int i=0; i < height; i++){
      for(int j=0; j < width; j++){
        co = o[i*width*z+j*z+0]\
             +256*o[i*width*z+j*z+1]\
             +65536*o[i*width*z+j*z+2];
        if(co==16777215){
          u[i*width+j] = rhobar;
        }
      }
    }

    /** Initialize the reference map coordinates. */
    double *X = malloc(height*width*2 * sizeof(double));
    double *cX = malloc(height*width*2 * sizeof(double));
    for(int i=0; i < height; i++){
      for(int j=0; j < width; j++){
        X[i*width*2+j*2+0] = h*i;
        X[i*width*2+j*2+1] = h*j;
      }
    }

    //printf("x: %f, y: %f\n", X[100*width*2+50*2+0], X[100*width*2+50*2+1]);

    // Calculate timestep size.
    double dt = 0.24*h*h;
    double T  = (height*height+width*width)/12.0;
    int nsteps = (int) ceil(T/dt);
    dt = T/nsteps;
    printf("Solving to T= %10f using %d timesteps.\n", T, nsteps);

    //get_time(&tend);
    tend = omp_get_wtime();
    printf("Elapsed time pre-processing: %f s\n", tend-tstart); //, timespec_diff(tstart, tend));
    //for(int i=0; i < height; i++){
    //  for(int j=0; j < width; j++){
    //    if (u[i*width + j]==0){
    //      printf("Zero observed for i=%d j=%d\n",i,j);
    //    }
    //  }
    //}
    //get_time(&tstart);
    tstart = omp_get_wtime();
    // Perform the integration timesteps, using the smaller
    // dt for the first few steps to deal with the large velocities
    // that initially occur.

    double time = 0;
    for(int l=0; l < 24; l++){
      step(dt/24.0, &time, u, cu, X, cX, h, ih2);
    }
    nsteps=2000;
    for(int l=1; l < nsteps;l++){
      step(dt, &time, u, cu, X, cX, h, ih2);
    }

    //get_time(&tend);
    tend = omp_get_wtime();
    printf("Elapsed time computing: %f s\n", tend-tstart); // timespec_diff(tstart, tend));


    //int i = 70;
    //int j = 150;

    //printf("for (%d, %d) X: %f, %f\n", i, j, X[i*width*2+j*2+0], X[i*width*2+j*2+1]);
    //printf("for (%d, %d) u: %f\n", i, j, u[i*width+j]);

    //get_time(&tstart);
    tstart = omp_get_wtime();

    // Use the deformed reference map to plot the density-equalized US map.
    int i2;
    int j2;
    //int o2[height*width*z];
    int *o2 = malloc(height*width*z * sizeof(int));

    for (int i=0; i<height; i++) {
        for (int j=0; j<width; j++) {
          i2=(int) X[i*width*2+j*2+0]+0.5;
          j2=(int) X[i*width*2+j*2+1]+0.5;

          if (i2<0) {
            i2 = 0;
            }else if(i2 > height-1){
            i2 = height-1;
          }
          if(j2 < 0){
            j2 = 0;
          } else if (j2>(width-1)) {
            j2= width-1;
          }
          o2[i*width*z+j*z+0] = o[i2*width*z+j2*z+0];
          o2[i*width*z+j*z+1] = o[i2*width*z+j2*z+1];
          o2[i*width*z+j*z+2] = o[i2*width*z+j2*z+2];
        }
    }

    //printf("%d, %d\n", i2,j2);

    // This function sets the pixel values to o2. The pixel parameters are
    // global vairables which are defined at the very top.

    for(int i = 0; i < height; i++) {
      png_bytep row = row_pointers[i];
      for(int j = 0; j < width; j++) {
        png_bytep py = &(row[j * 4]);
        py[0] = o2[i*width*z+j*z+0];
        py[1] = o2[i*width*z+j*z+1];
        py[2] = o2[i*width*z+j*z+2];
        py[3] = 255; // set the opacity of the image to 100 percent
      }
    }

    //get_time(&tend);
    tend = omp_get_wtime();
    printf("Elapsed time post-processing: %f s\n", tend-tstart); // timespec_diff(tstart, tend));

    //get_time(&tstart);
    tstart = omp_get_wtime();
    write_png_file("dens_eq.png");
    //get_time(&tend);
    tend = omp_get_wtime();
    printf("Elapsed time saving: %f s\n", tend-tstart); //timespec_diff(tstart, tend));


    return 0;

}
