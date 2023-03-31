int test(int* a_ptr, int b) {
    *a_ptr = b;
    return 0;
}

int main() {
    int a = 123;
    &a;
    *(&a);
    int* a_ptr = &a;
    test(a_ptr, 10);
    a;
    test(a_ptr, 20);
    a;
}