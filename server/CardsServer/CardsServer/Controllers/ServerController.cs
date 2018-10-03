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
        static extern bool draw_discard_to_table();

        [DllImport("cards_backend.so", CallingConvention = CallingConvention.Cdecl)]
        static extern bool draw_discard_to_hand(byte index);

        [DllImport("cards_backend.so", CallingConvention = CallingConvention.Cdecl)]
        static extern void put_table_json(byte[] buff);

        private static bool isActive = false;

        private static string[] players = new string[4];
        private static bool[] showHands = new bool[4];

        private static string tableJson;
        private static string displayNamesJson;

        // Updates the table obj JSON for GET at /api/table
        private void updateTableJson()
        {
            byte[] buff = new byte[800];
            put_table_json(buff);
            tableJson = "" + System.Text.Encoding.Default.GetString(buff).TrimEnd('\0');
        }

        // Updates the display names JSON for GET at /api/players
        private void updatePlayersJson()
        {
            displayNamesJson = "{\"players\" : [";
            for (int i = 0; i < players.Length; i++)
            {
                if (players[i] == null)
                {
                    displayNamesJson += 
                        "{ \"id\" : " + i +
                        ", \"name\" : \"null\"" + 
                        ", \"showHand\" : \"False\"}";
                }
                else
                {
                    displayNamesJson +=
                        "{ \"id\" : " + i +
                        ", \"name\" : \"" + players[i] +
                        "\", \"showHand\" : \"" + showHands[i].ToString() + "\"}";
                }

                if (i != players.Length - 1)
                {
                    displayNamesJson += ",";
                }
            }
            displayNamesJson += "]}";
        }

        // GET api/start
        public bool start()
        {
            if (!isActive)
            {
                construct_table(4);
                shuffle_main();
                updateTableJson();
                updatePlayersJson();
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
            for (int i = 0; i < players.Length; i++)
            {
                if (players[i] == null)
                {
                    players[i] = displayName;
                    updatePlayersJson();
                    return i.ToString();
                }
            }

            return (-1).ToString();
        }

        // GET api/unregister/{id}
        public bool unregisterPlayer(int id)
        {
            if (players[id] != null)
            {
                players[id] = null;
                showHands[id] = false;
                updatePlayersJson();
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

        // GET api/toggle_show_hand/{index}
        public bool toggleShowHand(int index)
        {
            showHands[index] = !showHands[index];
            updatePlayersJson();
            return showHands[index];
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
        
        // GET api/draw_discard_to_table
        public bool drawDiscardToTable()
        {
            if (isActive)
            {
                bool toReturn = draw_discard_to_table();
                updateTableJson();
                return toReturn;
            }
            return false;
        }
        
        // GET api/draw_discard_to_hand/{index}
        public bool drawDiscardToHand(int index)
        {
            if (isActive)
            {
                bool toReturn = draw_discard_to_hand((byte)index);
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
        public string getPlayersJson()
        {
            if (isActive)
            {
                return displayNamesJson;
            }
            return "ERR: Game not active.";
        }

    }
}