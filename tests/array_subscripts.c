int main()
{
    int b = 1;
    int c = 2;
    int *b_ptr = &b;
    // No negative indexes
    b_ptr[0];
    b_ptr[1];
    b_ptr[0] = b_ptr[0] + 2;
    b;
}