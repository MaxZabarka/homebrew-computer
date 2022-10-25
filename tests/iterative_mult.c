int mult(int a, int b) {
    int sum = 0;
    while (a) {
        sum = sum + b;
        a = a - 1;
    }
    return sum;
}


int main()
{
    mult(mult(2, 3), 5);
}