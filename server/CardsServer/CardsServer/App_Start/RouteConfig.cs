using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using System.Web.Routing;

namespace CardsServer
{
    public class RouteConfig
    {
        public static void RegisterRoutes(RouteCollection routes)
        {
            routes.MapRoute(
                "Start", "api/start", new { controller = "Server", action = "start" }
            );

            routes.MapRoute(
                "Shutdown", "api/shutdown", new { controller = "Server", action = "shutdown" }
            );

            routes.MapRoute(
                "Active", "api/active", new { controller = "Server", action = "active" }
            );

            routes.MapRoute(
                "Healthcheck", "api/healthcheck", new { controller = "Server", action = "healthcheck" }
            );

            routes.MapRoute(
                "Register", "api/register/{displayName}", new { controller = "Server", action = "registerNewPlayer" }
            );

            routes.MapRoute(
                "Unregister", "api/unregister/{id}", new { controller = "Server", action = "unregisterPlayer" }
            );

            routes.MapRoute(
                "Reset", "api/reset", new { controller = "Server", action = "reset" }
            );

            routes.MapRoute(
                "ToggleShowHand", "api/toggle_show_hand/{index}", new { controller = "Server", action = "toggleShowHand" }
            );

            routes.MapRoute(
                "DrawMainToTable", "api/draw_main_to_table", new { controller = "Server", action = "drawMainToTable" }
            );

            routes.MapRoute(
                "DrawMainToHand", "api/draw_main_to_hand/{index}", new { controller = "Server", action = "drawMainToHand" }
            );

            routes.MapRoute(
                "DrawHandToTable", "api/draw_hand_to_table/{hand_index}/{card_index}", new { controller = "Server", action = "drawHandToTable" }
            );

            routes.MapRoute(
                "DrawTableToHand", "api/draw_table_to_hand/{hand_index}/{card_index}", new { controller = "Server", action = "drawTableToHand" }
            );

            routes.MapRoute(
                "DrawTableToDiscard", "api/draw_table_to_discard/{index}", new { controller = "Server", action = "drawTableToDiscard" }
            );

            routes.MapRoute(
                "DrawHandToDiscard", "api/draw_hand_to_discard/{hand_index}/{card_index}", new { controller = "Server", action = "drawHandToDiscard" }
            );

            routes.MapRoute(
                "DrawDiscardToTable", "api/draw_discard_to_table", new { controller = "Server", action = "drawDiscardToTable" }
            );

            routes.MapRoute(
                "DrawDiscardToHand", "api/draw_discard_to_hand/{index}", new { controller = "Server", action = "drawDiscardToHand" }
            );

            routes.MapRoute(
                "TableJSON", "api/table", new { controller = "Server", action = "getTableJson" }
            );

            routes.MapRoute(
                "PlayersJSON", "api/players", new { controller = "Server", action = "getPlayersJson" }
            );

        }
    }
}
