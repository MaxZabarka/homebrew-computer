int mult(int x, int y)
{
    if (y == 0)
    {
        return 0;
    }
    return x + mult(x, y - 1);
}

int main()
{
    // // 44
    // mult(50, 6);

    // 30
    mult(mult(2, 3), 5);

    // stack overflow
    // mult(2, 40);
}