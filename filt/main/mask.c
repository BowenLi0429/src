#include <float.h>

#include <rsf.h>

int main(int argc, char* argv[]) {
    int *ibuf;
    size_t nsiz, nbuf, j;
    float *fbuf, min, max;
    sf_file in, out;

    sf_init (argc, argv);
    in = sf_input("in");
    out = sf_output("out");

    if (SF_FLOAT != sf_gettype(in)) sf_error("Need float input");
    sf_settype(out,SF_INT);

    nbuf = BUFSIZ/sizeof(float);
    fbuf = sf_floatalloc (nbuf);
    ibuf = sf_intalloc (nbuf);

    if (!sf_getfloat("min",&min)) min=-FLT_MAX;
    if (!sf_getfloat("max",&max)) max=+FLT_MAX;

    for (nsiz = sf_filesize (in); nsiz > 0; nsiz -= nbuf) {
	if (nbuf > nsiz) nbuf=nsiz;

	sf_read(fbuf,sizeof(float),nbuf,in);
	for (j=0; j < nbuf; j++) {
	    ibuf[j] = (fbuf[j] <= max && fbuf[j] >= min);
	}
	sf_write(ibuf,sizeof(int),nbuf,out);
    }
}
	    
