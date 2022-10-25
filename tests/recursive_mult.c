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
    mult(mult(2, 3), 5);
}