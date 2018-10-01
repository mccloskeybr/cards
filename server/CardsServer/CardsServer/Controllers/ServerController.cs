using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Web;
using System.Web.Mvc;
using Aws.GameLift.Server;
using CardsServer.App_Data;

namespace CardServer.Controllers
{
    public class ServerController : Controller
    {
        [DllImport("cards_backend.so", CallingConvention = CallingConvention.Cdecl)]
        static extern void construct_table(byte numHands);

        [DllImport("cards_backend.so", CallingConvention = CallingConvention.Cdecl)]
        static extern void destroy_table();

        [DllImport("cards_backend.so", CallingConvention = CallingConvention.Cdecl)]
        static extern void reset_table();

        [DllImport("cards_backend.so", CallingConvention = CallingConvention.Cdecl)]
        static extern void shuffle_main();

        [DllImport("cards_backend.so", CallingConvention = CallingConvention.Cdecl)]
        static extern bool draw_main_to_table();

        [DllImport("cards_backend.so", CallingConvention = CallingConvention.Cdecl)]
        static extern bool draw_main_to_hand(byte index);

        [DllImport("cards_backend.so", CallingConvention = CallingConvention.Cdecl)]
        static extern bool draw_hand_to_table(byte hand_index, byte card_index);

        [DllImport("cards_backend.so", CallingConvention = CallingConvention.Cdecl)]
        static extern bool draw_table_to_hand(byte hand_index, byte card_index);

        [DllImport("cards_backend.so", CallingConvention = CallingConvention.Cdecl)]
        static extern void put_table_json(byte[] buff);

        private static bool active = false;
        private static bool[] playerSlots = new bool[4];

        // GET api/start
        public bool start()
        {
            if (!active)
            {
                construct_table(4);
                active = true;
                return true;
            }

            return false;
        }

        // GET api/shutdown
        public bool shutdown()
        {
            if (active)
            {
                destroy_table();
                active = false;

                return true;
            }

            return false;
        }

        // GET api/healthcheck
        public bool healthcheck()
        {
            return true;
        }

        // GET api/register
        public string registerNewPlayer(String playerSessionId)
        {
            for (int i = 0; i < playerSlots.Length; i++)
            {
                if (playerSlots[i] == false)
                {
                    playerSlots[i] = true;
                    return i.ToString();
                }
            }

            return (-1).ToString();
        }

        // GET api/unregister/{id}
        public bool unregisterPlayer(int id)
        {
            if (playerSlots[id] == true)
            {
                playerSlots[id] = false;
                return true;
            }

            return false;
        }

        // GET api/reset
        public bool reset()
        {
            if (active)
            {
                reset_table();
                return true;
            }

            return false;
        }

        // GET api/shuffle
        public bool shuffle()
        {
            if (active)
            {
                shuffle_main();
                return true;
            }

            return false;
        }

        // GET api/draw_main_to_table
        public bool drawMainToTable()
        {
            if (active)
            {
                return draw_main_to_table();
            }
            return false;
        }

        // GET api/draw_main_to_hand/{index}
        public bool drawMainToHand(int index)
        {
            if (active)
            {
                return draw_main_to_hand((byte)index);
            }
            return false;
        }

        // GET api/draw_hand_to_table/{hand_index}/{card_index}
        public bool drawHandToTable(int hand_index, int card_index)
        {
            if (active)
            {
                return draw_hand_to_table((byte)hand_index, (byte)card_index);
            }
            return false;
        }

        // GET api/draw_table_to_hand/{hand_index}/{card_index}
        public bool drawTableToHand(int hand_index, int card_index)
        {
            if (active)
            {
                return draw_table_to_hand((byte)hand_index, (byte)card_index);
            }
            return false;
        }

        // GET api/table
        public string getTableJson()
        {
            if (active)
            {
                byte[] buff = new byte[760];
                put_table_json(buff);
                return "" + System.Text.Encoding.Default.GetString(buff).TrimEnd('\0');
            }
            return "ERR: Game not active.";
        }

    }
}