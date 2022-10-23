// int sub(int a, int b, int c)
// {
//     return a - b + c;
// }
// int add(int a, int b)
// {
//     return a + a - sub(1, b, a);
// }
// int test(int n)
// {
//     return test(n - 1) + test(n - 2);
//     // int a = 3;
//     // int b = 30;
//     // int c = 7;
//     // return b - a + c;
// }
int mult(int x, int y) {
    if (y == 0) {
        return 0;
    }
    return x + mult(x, y -1);

}

int main()
{
    mult(5, 30);
    // 55 | 88;
    // 88 | 55;
    // 10 | 40;
    // 0  | 0;
    // 127 | 127;
    // fib(5);
    // test(5);
    // int b;
    // b = 5;
    // 5+10;
    // b + 10;
    // 10;
    // int a;
    // int c;
    // int a;
    // int b;
    // int a = 5;
    //    (10 - (4 - 1)) ;
    // add(15, 3) + !0 + 70;
    // 5 | 5;
    // 4 | 4;
    // 88 | 55;
    // 5;

    // (add(15, 3) + !0 + 70) | 55;
    // 5;

    // (10 + (3 - 7) + (4 - 1));
    // (10 - 7 + 3 + (4 - 1) - 1) + 1 + 3 - 1 ;
    // int* c = 5;
}