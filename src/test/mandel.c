int main() {
  int n;
  float r, i, R, I, b;
  for (i = -1.0; i < 1.0; i += 0.06) {
    for (r = -2.0; (I = i), (R = r) < 1.0; r += 0.03) {
      for (n = 0; (b = I * I), 26 > n++ && R * R + b < 4.0;) {
        I = 2.0 * R * I + i;
        R = R * R - b + r;
      }
      n > 20 ? printf("#") : printf(".");
    }
    printf("\n");
  }
}
