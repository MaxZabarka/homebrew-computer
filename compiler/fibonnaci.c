int main()
{
    int n = 0;
    int first = 0;
    int second = 1;
    int result;
    int i = 0;
    while (i < n)
    {
        result = first + second;
        first = second;
        second = result;
        i = i + 1;
    }
    return result;
}
