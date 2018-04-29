# Prime-Number-Image-Generator
finds a prime number which represents the input image
 
Dithers the image into a black and white format (10 shades for 10 digits) with added noise.  
This results in a random (width * height) digit number which looks like the input image. Because of the prime number theorem we should be able to find a prime in ln(10^(width * height)) trials i.e. for a 128 * 128 image, 36k trials. 
The python script only generates odd numbers doubling the chances.

Using the highly optimised (gnu mp based, assembly tuned) mpir library, with the rabin miller primality test it can fairly quickly filter down the generated prime candidate dataset, finding a prime number.



 *16k digit prime number as 128 * 128 matrix*
![alt text][16k_num_image]


*0 as 0x000000 and 9 as 0xffffff*  
![alt text][16k_prime_image] 


[16k_num_image]: https://github.com/LengyelR/Prime-Number-Image-Generator/blob/master/readme/16_prime_as_num.JPG "Image as bw mtx"
[16k_prime_image]: https://github.com/LengyelR/Prime-Number-Image-Generator/blob/master/readme/16k_prime.jpg "16k digit prime image"
