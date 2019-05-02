#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <png.h>

/** Finds the index of string na in string array c. */
static int getStringIndex(char (*c)[256], char *na, int SIZE)
{
    for(int j=0; j < SIZE; j++){
        if(strcmp(na,c[j]) == 0){
          return j;
        }
    }
    return 0;
}

/** Finds index of el in int array c. */
static int getIntIndex(int *c, int  el, int SIZE)
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
    //int y;

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

int* read_map(char* pngfile, int* m, int* n)
{
  /* Read in the undeformed US map. */
  read_png_file(pngfile);

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

  *m = height;
  *n = width;

  return o;

}

void image_to_density_map(int* o, double* u, char* colorfile, char* densityFile, int numentities, int rank) {

        // Read in the color values for each state.
        //char const* const fileName = "colchart.txt";
        FILE* file = fopen(colorfile, "r");
        char line[256];
        int d[numentities];
        char c[numentities][256];
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

            // Read in the three color channels.
            int re = atoi(a[0]);
            int gr = atoi(a[1]);
            int bl = atoi(a[2]);

            /** Read in the name of the state, taking care to handle to
              * states space in them. */
            char na[256];
            if(*a[4]=='\0'){
                strcpy(na, a[3]);
            }else{
                strcpy(na, a[3]);
                strcat(na, " ");
                strcat(na, a[4]);
            }
            strcpy(c[k], na);

            /** Encode the color into a single integer, and store the information. */
            int nu = re+256*gr+65536*bl;
            d[k] = nu;
            k+=1;
        }

        fclose(file);

        // Read in the population densities for each state.
        // char const* const fileName2 = "density.txt";
        FILE* file2 = fopen(densityFile, "r");
        double rh[numentities];

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
            int m = getStringIndex(c, na, numentities);
            rh[m] = atoll(a[0]);
        }

        /** TESTING
          * c  - string array for the name of the states
          * d  - unique bar code for each state (RGB) = R+256*G+65536*B
          * rh[k] - population density of state c[k]. */
        /**
          for(int j=0; j<SIZE; j++){
          printf("%s, %d, %f\n", c[j], d[j], rh[j]);
        }*/

        /** Scan the image to set the density field in the states.
          * In addition, calculate the average density. */
        //double *u = malloc(height*width * sizeof(double));
        double srho = 0.0;
        int npts = 0;
        int co;
        int index;

        int z = 3;
        for(int i=0; i < height; i++){
          for(int j=0; j < width; j++){
            co = o[i*width*z+j*z+0]+256*o[i*width*z+j*z+1]+65536*o[i*width*z+j*z+2];
            index = getIntIndex(d, co, numentities);
            if (index != -1){
              u[i*width+j] = rh[index];
              srho+=u[i*width+j];
              npts+=1;
            }
            else if(co != 16777215){
              abort();
            }
          }
    }

      /* Re-scan over the image to set the average density
         in regions outside the states. */
      double rhobar=srho/npts;
      if(rank==0){
        printf("Avg. rho: %f\n", rhobar);
      }
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

}

void save_map(int* o, double* X){

      /** Use the deformed reference map to plot the density-equalized US map. */
      int i2;
      int j2;
      int z = 3;
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

      /* This function sets the pixel values to o2. The pixel parameters are
         global vairables which are defined at the very top. */
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

      write_png_file("dens_eq.png");
}
