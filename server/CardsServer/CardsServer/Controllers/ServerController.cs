using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Web;
using System.Web.Mvc;
using Aws.GameLift.Server;

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
        static extern bool draw_table_to_discard(byte index);

        [DllImport("cards_backend.so", CallingConvention = CallingConvention.Cdecl)]
        static extern bool draw_hand_to_discard(byte hand_index, byte card_index);

        [DllImport("cards_backend.so", CallingConvention = CallingConvention.Cdecl)]
        static extern void put_table_json(byte[] buff);

        private static bool isActive = false;
        private static string[] playerSlots = new string[4];
        private static string tableJson;

        // Updates the table obj JSON for GET at /api/table
        private void updateTableJson()
        {
            byte[] buff = new byte[800];
            put_table_json(buff);
            tableJson = "" + System.Text.Encoding.Default.GetString(buff).TrimEnd('\0');
        }

        // GET api/start
        public bool start()
        {
            if (!isActive)
            {
                construct_table(4);
                shuffle_main();
                updateTableJson();
                isActive = true;
                return true;
            }

            return false;
        }

        // GET api/shutdown
        public bool shutdown()
        {
            if (isActive)
            {
                destroy_table();
                isActive = false;
                return true;
            }

            return false;
        }

        // GET api/active
        public bool active()
        {
            return isActive;
        }

        // GET api/healthcheck
        public bool healthcheck()
        {
            return true;
        }

        // GET api/register
        public string registerNewPlayer(String displayName)
        {
            for (int i = 0; i < playerSlots.Length; i++)
            {
                if (playerSlots[i] == null)
                {
                    playerSlots[i] = displayName;
                    return i.ToString();
                }
            }

            return (-1).ToString();
        }

        // GET api/unregister/{id}
        public bool unregisterPlayer(int id)
        {
            if (playerSlots[id] != null)
            {
                playerSlots[id] = null;
                return true;
            }

            return false;
        }

        // GET api/reset
        public bool reset()
        {
            if (isActive)
            {
                reset_table();
                shuffle_main();
                updateTableJson();
                return true;
            }

            return false;
        }

        // GET api/draw_main_to_table
        public bool drawMainToTable()
        {
            if (isActive)
            {
                bool toReturn = draw_main_to_table();
                updateTableJson();
                return toReturn;
            }
            return false;
        }

        // GET api/draw_main_to_hand/{index}
        public bool drawMainToHand(int index)
        {
            if (isActive)
            {
                bool toReturn = draw_main_to_hand((byte)index);
                updateTableJson();
                return toReturn;
            }
            return false;
        }

        // GET api/draw_hand_to_table/{hand_index}/{card_index}
        public bool drawHandToTable(int hand_index, int card_index)
        {
            if (isActive)
            {
                bool toReturn = draw_hand_to_table((byte)hand_index, (byte)card_index);
                updateTableJson();
                return toReturn;
            }
            return false;
        }

        // GET api/draw_table_to_hand/{hand_index}/{card_index}
        public bool drawTableToHand(int hand_index, int card_index)
        {
            if (isActive)
            {
                bool toReturn = draw_table_to_hand((byte)hand_index, (byte)card_index);
                updateTableJson();
                return toReturn;
            }
            return false;
        }

        // GET api/draw_table_to_discard/{index}
        public bool drawTableToDiscard(int index)
        {
            if (isActive)
            {
                bool toReturn = draw_table_to_discard((byte)index);
                updateTableJson();
                return toReturn;
            }
            return false;
        }

        // GET api/draw_hand_to_discard/{hand_index}/{card_index}
        public bool drawHandToDiscard(int hand_index, int card_index)
        {
            if (isActive)
            {
                bool toReturn = draw_hand_to_discard((byte)hand_index, (byte)card_index);
                updateTableJson();
                return toReturn;
            }
            return false;
        }

        // GET api/table
        public string getTableJson()
        {
            if (isActive)
            {
                return tableJson;
            }
            return "ERR: Game not active.";
        }


        // GET api/displaynames
        public string getDisplayNamesJson()
        {
            if (isActive)
            {
                string json = "{\"names\":[";
                for (int i = 0; i < playerSlots.Length; i++)
                {
                    if (playerSlots[i] == null)
                    {
                        json += "\"empty\"";
                    }
                    else
                    {
                        json += "\"" + playerSlots[i] + "\"";
                    }

                    if (i != playerSlots.Length - 1)
                    {
                        json += ",";
                    }
                }
                json += "]}";
                return json;
            }
            return "ERR: Game not active.";
        }

    }
}