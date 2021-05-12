void removeChar(char *str, char garbage) 
{
    char *src, *dst;
    for (src = dst = str; *src != '\0'; src++) 
    {
        *dst = *src;
        if (*dst != garbage) dst++;
    }
    *dst = '\0';
}

char* toLower(char* s) {
    char *p;
    for(p=s; *p; p++) *p=tolower(*p);
    return s;
}
