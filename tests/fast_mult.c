int mult(int x, int y)
{
    // UB! this is not initialized to zero because there is not enough space in the ROM. If it happens to be anything but a zero the program will not work
    int sum; 
    int i = 8;
    while (i)
    {
        i = i - 1;
        if ((y << i) & 0b10000000)
        {
            sum = sum + x;
        }
        x = x << 1;
    }
    return sum;
}

int main()
{
    mult(255, 255);
}