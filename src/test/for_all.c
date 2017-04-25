int sum = 0;

void test_sum(){
    if(sum == 45)
        printf("Ok!\n");
    else
        printf("Wrong!\n");
    sum = 0;
}

int main(){ 
    int x;
    
    for(int x; x < 10; x++)
        sum += x;
        
    test_sum();

    for(x = 0; x < 10; x++)
        sum += x;
        
    test_sum();

    x = 0;
    for(;x < 10; x++)
        sum += x;
        
    test_sum();

    x = 0;
    for(;; x++){
        if( x >= 10) break;
        sum += x;
    }
        
    test_sum();

    x = 0;
    for(;;){
        if( x >= 10) break;
        sum += x;
        x++;
    }
        
    test_sum();
    
    x = 0;
    for(;x < 10;){
        sum += x;
        x++;
    }
        
    test_sum();

    sum = 0;

    for(int x = 0;;x++){
        if( x >= 10) break;
        sum += x;
    }
        
    test_sum();

    for(x = 0;;x++){
        if( x >= 10) break;
        sum += x;
    }
        
    test_sum();

    sum = 0;

    for(int x = 0;x < 10;){
        sum += x;
        x++;
    }
        
    test_sum();

    sum = 0;

    for(x = 0;x < 10;){
        sum += x;
        x++;
    }
        
    test_sum();

    for(int x;;){
        if( x >= 10) break;
        sum += x;
        x++;
    }
        
    test_sum();

    for(x = 0;;){
        if( x >= 10) break;
        sum += x;
        x++;
    }
        
    test_sum();
        
    return 0;
}
