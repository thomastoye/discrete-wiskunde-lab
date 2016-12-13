using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Numerics;

namespace RSA
{
    class Program
    {
        static void Main(string[] args)
        {
            int n = 125291;
            int eA = 5;
            int eB = 13;
            int c = 96207;

            //n = 391;
            //eA = 5;
            //c = 319;


            //ReadData();
            FindMessage(n, eA, eB, c);
        }

        /* To read date from cmd
        private static void ReadData()
        {
            Console.Write("n: ");
            int.TryParse(Console.ReadLine(), out n);

            Console.Write("eA: ");
            int.TryParse(Console.ReadLine(), out eA);

            Console.Write("eB: ");
            int.TryParse(Console.ReadLine(), out eB);

            Console.Write("c: ");
            int.TryParse(Console.ReadLine(), out c);
        }
        */

        private static void FindMessage(int n, int eA, int eB, int c)
        {
            // ------------------------------
            //  STAP 1: Prime factors
            // ------------------------------
            Console.WriteLine(" --> STAP 1: Prime factors\n");
            int p = FindPrimeFactor(n);
            int q = n / p;
            int phi = (p - 1) * (q - 1);

            Console.WriteLine("p = " + p);
            Console.WriteLine("q = " + q);
            Console.WriteLine("phi = " + phi);


            // ------------------------------
            //  STAP 2: Bezout
            // ------------------------------
            Console.WriteLine("\n\n --> STAP 2: Bezout\n");
            int inverse = FindInverseWithBezout(eA, phi);
            int inverse2 = FindInverseWithBezout2(eA, phi);

            int test = FindInverseWithBezout(3,10);
            int test2 = FindInverseWithBezout2(3,10);
            Console.WriteLine("TEST: " + test);
            Console.WriteLine("TEST2: " + test2);

            int dA = inverse % phi;
            Console.WriteLine("dA = " + dA);

            //extra controle  x * x^(-1) = 1 mod phi
            int one = (inverse * eA) % phi;
            Console.WriteLine("This should be one: " + one);


            // ------------------------------
            //  STAP 3: Bereken m
            // ------------------------------
            Console.WriteLine("\n\n --> STAP 3: Bereken m\n");

            BigInteger m = BigInteger.ModPow(c, dA, n);
            Console.WriteLine("c^dA mod n = " + m);

            BigInteger controleVanC = BigInteger.ModPow(m, dA * eA, n);
            Console.WriteLine("c = m mod n = m^(eB*dA) mod n = " + controleVanC); // <--- ???? klopt die formule ????

           
            //int cInverse = FindInverseWithBezout(c, n);
            //Console.WriteLine("cInverse = " + cInverse);



            Console.ReadKey();
        }

        static long mod(long a, int n)
        {
            return ((a % n) + n) % n;
        }

        private static int FindPrimeFactor(int n)
        {
            int primeFactor = 1;

            //test alle delers i waarvoor geldt: (2 <= i <= n-1)
            for (int i = 2; i <= n - 1; i++)
            {
                if (n % i == 0)
                {
                    primeFactor = i;
                    return primeFactor;
                }

                primeFactor++;
            }

            //onderling ondeelbaar
            return 1;
        }


        //ggd(e, phi) = 1  
        //dA * eA = 1  mod(phi)  <==> dA = eA^(-1) mod(phi)
        private static int FindInverseWithBezout(int a, int b)
        {
            Console.WriteLine(String.Format("gdd({0}, {1})", a, b));

            List<int[]> test = new List<int[]>();

            int gcd = a;
            //zolang de rest niet gelijk is aan 0
            while (a != 0)
            {
                int q = b / a;
                int r = b % a;
                Console.Write(String.Format(" = ggd({0}, {1} mod {0})", a, b));            // ggd(a, b mod a)         
                Console.WriteLine(String.Format("\t {1} = {0} * {2} + {3}", a, b, q, r));  // b = a*q+r

                test.Add(new int[] { b, a, q, r });
                b = a; // b will be ggd in last step
                a = r;
            }

            /* OWN IMPLEMENTATION
            * b1 = a1 * q1 + r1     (-> b2=a1, a2=r1)
            * b2 = a2 * q2 + r2     (-> b3=a2, a3=r2)   ---> r2 will be 1 
            * b3 = a3 * q3 + r3
            * 
            * BEZOUT: 1 = alpha * a + beta * b      ==> alpha, beta zijn de bezout getallen
            * start from row 2 where r2 = 1
            * r2 = 1 = b2 - a2 * q2
            *      1 = a1 - (b1 - a1 * q1) * q2
            *      1 = (1 + q1q2)*a1 + (-q2)*b1;
            */

            // IF REST IS ZERO!! 
            int q1, q2;
            int alpha, beta;
            int r1 = test[0][3];
            if (r1 == 1)
            {
                //ggd takes 2 steps 
                //==> r1 = 1 = b1 - a1 * q1
                //         1 = (-q1)*a1
                q1 = 
            }
            else
            {
                //ggd takes 3 steps
                q1 = test[0][2];
                q2 = test[1][2];
                alpha = 1 + q1 * q2;
                beta = -q2;
            }

         
            Console.WriteLine(String.Format("1: alpha={0}, beta={1}, gcd={2}", alpha, beta, b));


            int inverse = alpha;
            return inverse;
        }


        /*
        * @url1: http://stackoverflow.com/questions/27004830/how-to-write-extended-euclidean-algorithm-code-wise-in-java
        * @url2: https://comeoncodeon.wordpress.com/2011/10/09/modular-multiplicative-inverse/
        */
        private static int FindInverseWithBezout2(int a, int b)
        {
            int x0 = 1; int y0 = 0;
            int xn = 0; int yn = 1;

            int[] list1 = new int[] { a, x0, xn };
            int[] list2 = new int[] { b, y0, yn };
            int[] list3 = new int[3];

            while (list1[0] - list2[0] * (list1[0] / list2[0]) > 0)
            {
                for (int i = 0; i < 3; i++) list3[i] = list2[i];
                int q = list1[0] / list2[0];
                for (int i = 0; i < 3; i++) list2[i] = list1[i] - list2[i] * q;
                for (int i = 0; i < 3; i++) list1[i] = list3[i];
            }

            int gcd = list2[0]; //this will be 1
            int alpha = list2[1]; //this is the inverse element
            int beta = list2[2];
            Console.WriteLine(String.Format("2: alpha={0}, beta={1}, gcd={2}", alpha, beta, gcd));


            int inverse = alpha;
            return inverse;
        }
    }
}
