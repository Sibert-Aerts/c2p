// file full of bizarre grammatically correct scenarios

void **const*const* main(void flup[99][100], int x, const const float y, char (*blub)[]){

    // empty
    ;;;;;;
    {}{}{}
    {{{}}}

    // pointless
    "fifteen";
    15;
    fifteen;
    "the number", is, "fifteen";
    15.0e15;


    // repetitive
    const const int const;
    char *** pointer;
    float (*const(*const(*const x[10])[10])[10])[10];
    x + + + 1;
    y - - - 1;
    ------x;
    y++++++;
    ((x));
    f(f(f()));
    (const int*const)(const int*const)x;
    int(((x)));

    // convoluted
    a ? b ? c ? d ? e ? f : g : h : i : j : k;
    a = b = c = d = e = f;
    a = b , c = d , e = f;
    a+++b---c+++d---e+++f;
    a* *b* *c* *d* *e* *f;
    (a, b, c)   (d, e, f);
     (a)(b)(c)(d)(e)(f);
     (a(b(c(d(e(f))))));

}
