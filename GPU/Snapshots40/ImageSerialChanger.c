#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <png.h>
#include <math.h>

// Number of states/entities to calculates:
#define SIZE 3142


static int getStringIndex(char (*c)[256], char *na)
{
    for(int j=0; j < SIZE; j++){
        if(strcmp(na,c[j]) == 0){
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
int main(){

    char const* const fileName = "colchart_counties.txt";
    FILE* file = fopen(fileName, "r");
    char line[256];
    int d[SIZE] = {0};
    int c[SIZE] = {0};
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
        //strcpy(c[k], na);
        int fips =atoi(a[3]);
        c[k] = fips;
//        printf("c[%d]=%d\n",k,c[k]);
        /** Encode the color into a single integer, and store the information. */
        int nu = re+256*gr+65536*bl;
        d[k] = nu;
        k+=1;
    }

    fclose(file);
    char const* const fileName_dem = "Dem2016.txt";
    FILE* file_dem = fopen(fileName_dem, "r");
    char line_dem[256];
    int d_dem[SIZE] = {0};
    int c_dem[SIZE] = {0};
    int k_dem=0;

    while (fgets(line_dem, sizeof(line_dem), file_dem)) {
        char *token = strtok(strtok(line_dem,"\n"), " ");
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
        int fips =atoi(a[3]);
        c_dem[k_dem] = fips;
        //strcpy(c_dem[k], na);

        /** Encode the color into a single integer, and store the information. */
        int nu = re+256*gr+65536*bl;
        d_dem[k_dem] = nu;
//        printf("c_dem[%d]=%d\n",k,c_dem[k_dem]);
        k_dem+=1;
    }

    fclose(file_dem);

    char fname[100];
    char ffname[100];
    for (int idx_img=1; idx_img<380; idx_img++){
      printf("Image %d\n",idx_img);
      sprintf(fname,"time%04d.png",idx_img);
      read_png_file(fname);
      int z = 3;
      int *o = malloc(height*width*z * sizeof(int));
      for(int i = 0; i < height; i++) {
        png_bytep row = row_pointers[i];
        for(int j = 0; j < width; j++) {
          png_bytep py = &(row[j * 4]);
          int re=py[0];
          int gr=py[1];
          int bl=py[2];
          int nu = re+256*gr+65536*bl;
          if (re==255&&gr==255&&bl==255){
            o[i*width*z+j*z+0] = 255;
            o[i*width*z+j*z+1] = 255;
            o[i*width*z+j*z+2] = 255;
          }
          else{
            for (int kk=0; kk<SIZE; kk++){
              if (d[kk]==nu){
  //              printf("Im in\n");
                for(int ll=0; ll<SIZE+1; ll++){
                  if(c_dem[ll]==c[kk]){
                    int new_nu = d_dem[ll];
                    int bl_ = (int) new_nu/65536;
                    int gr_ = (int) (new_nu-65536*bl)/256;
                    int re_ = (int) new_nu-65536*bl-256*gr;
                    o[i*width*z+j*z+0] = re_;
                    o[i*width*z+j*z+1] = gr_;
                    o[i*width*z+j*z+2] = bl_;
  //                  printf("Eureka\n");
                    break;
                  }
                  if (ll==SIZE){
                    printf("Not found for nu=%d and fips=%d\n",nu, c[kk]);
                  }
                }
                break;
              }
            }
          }
        }
      }
      for(int i = 0; i < height; i++) {
        png_bytep row = row_pointers[i];
        for(int j = 0; j < width; j++) {
          png_bytep py = &(row[j * 4]);
          py[0] = o[i*width*z+j*z+0];
          py[1] = o[i*width*z+j*z+1];
          py[2] = o[i*width*z+j*z+2];
          py[3] = 255; // set the opacity of the image to 100 percent
        }
      }
      sprintf(ffname,"ftime%04d.png",idx_img);
      write_png_file(ffname);
      free(o);
    }
    return 0;


}
