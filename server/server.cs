using System;
using System.IO;
using System.Runtime.InteropServices;

namespace server {

    class Server
    {
        [DllImport("cards_backend.so")]
        static extern void construct_table(byte numHands);

	[DllImport("cards_backend.so")]
	static extern void shuffle_main();

        static void Main(string[] args)
        {
	    construct_table(1);
	    shuffle_main();

            Console.WriteLine("hello");
        }
    }

}
