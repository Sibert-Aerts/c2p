int a = 100;
int b = 100;
int c = 100;
int d = 100;
int e = 100;

int main(){
    int x = 200;
    int y = 200;
    int z = 200;
    
    int b = 200;
    
    d = 200;
    {
        int i = 300;
        
        int c = 300;
        int y = 300;
        
        z = 300;
        e = 300;
    }
}

/*
    This gives the following structure in the p-machine:
	[9]	        [i]	100     // global a
	[10]		[i]	100     // global b
	[11]		[i]	100     // global c
	[12]		[i]	200     // global d
	[13]		[i]	300     // global e
    ...
	[19]		[i]	200     // main x
	[20]		[i]	200     // main y
	[21]		[i]	300     // main z
	[22]		[i]	200     // main b
	[23]		[i]	300     // scoped i
	[24]		[i]	300     // scoped c
	[25]		[i]	300     // scoped y

/*
