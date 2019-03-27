#include <stdio.h>
#include <stdlib.h>
#include <math.h>

//In real working code these should be done more carefully
// to ensure no inconsistency in values
const long small_primes_len = 20;
const long small_primes[20] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71};
const long max_small_prime = 71;

char check_prime(long num);

  char check_prime(long num){

    char result;
    long index, end;

    end = ceil(sqrt((double) num));

    result = 1;
    //First check against the small primes
    for(index = 0; index < small_primes_len; index++){
      if (small_primes[index] == num) return 1;
      if (num%small_primes[index] == 0){
        return 0;
      }
    }

    //Test higher numbers, skipping all the evens
    for (index = max_small_prime + 2; index <= end; index += 2){
      if (num%index == 0){
        return 0;
      }
    }
    return result;
  }


long primes_in_range(long lower, long upper){

  long total;
  long i;

  total = 0;
  //Start with an odd number
  if(lower%2 == 0) lower = lower + 1;

  for(i = lower; i<= upper; i++){

    //We should get back either 0 or 1, 1 if prime
    total = total + check_prime(i);
  }

  return total;
}
