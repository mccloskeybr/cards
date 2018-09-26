﻿using System;
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
                "Healthcheck", "api/healthcheck", new { controller = "Server", action = "healthcheck" }
            );

            routes.MapRoute(
                "Reset", "api/reset", new { controller = "Server", action = "reset" }
            );

            routes.MapRoute(
                "Shuffle", "api/shuffle", new { controller = "Server", action = "shuffle" }
            );

            routes.MapRoute(
                "DrawMainToTable", "api/draw_main_to_table/{index}", new { controller = "Server", action = "drawMainToTable" }
            );

            routes.MapRoute(
                "DrawMainToHand", "api/draw_main_to_table/{hand_index}/{card_index}", new { controller = "Server", action = "drawMainToHand" }
            );

            routes.MapRoute(
                "DrawHandToTable", "api/draw_hand_to_table/{hand_index}/{card_index}", new { controller = "Server", action = "drawHandToTable" }
            );

            routes.MapRoute(
                "DrawTableToHand", "api/draw_table_to_hand/{hand_index}/{card_index}", new { controller = "Server", action = "drawTableToHand" }
            );

            routes.MapRoute(
                "TableJSON", "api/table", new { controller = "Server", action = "getTableJson" }
            );

        }
    }
}