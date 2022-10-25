int test() {
    return 1;
}
int test_2() {
    return 2;
}

int main() {
    test();
    test_2();
    test() + test_2();

}