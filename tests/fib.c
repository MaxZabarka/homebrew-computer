int fib(int n)
{
    if (n < 2)
    {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}
int main()
{
    fib(8);
    fib(5);
}