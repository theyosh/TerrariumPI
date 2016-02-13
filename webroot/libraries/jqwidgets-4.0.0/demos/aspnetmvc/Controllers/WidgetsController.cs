using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace jQWidgetsMVCDemo.Controllers
{
    public class WidgetsController : Controller
    {
        //
        // GET: /Widgets/
        public ActionResult Index()
        {
            return View("Grid");
        }

        // GET: /Widgets//Grid
        public ActionResult Grid(string theme)
        {
            ViewData["Theme"] = theme;
            return View("Grid");
        }

        // GET: /Widgets//TreeGrid
        public ActionResult TreeGrid(string theme)
        {
            ViewData["Theme"] = theme;
            return View("TreeGrid");
        }

        // GET: /Widgets//ListBox
        public ActionResult ListBox(string theme)
        {
            ViewData["Theme"] = theme;
            return View("ListBox");
        }

        // GET: /Widgets//ComboBox
        public ActionResult ComboBox(string theme)
        {
            ViewData["Theme"] = theme;
            return View("ComboBox");
        }

        // GET: /Widgets//DataTable
        public ActionResult DataTable(string theme)
        {
            ViewData["Theme"] = theme;
            return View("DataTable");
        }

        // GET: /Widgets//Chart
        public ActionResult Chart(string theme)
        {
            return View("Chart");
        }

        // GET: /Widgets//DropDownList
        public ActionResult DropDownList(string theme)
        {
            ViewData["Theme"] = theme;
            return View("DropDownList");
        }

        // GET: /Widgets//TreeWithCheckboxes
        public ActionResult TreeWithCheckboxes(string theme)
        {
            ViewData["Theme"] = theme;
            return View("TreeWithCheckboxes");
        }

        // GET: /Widgets//Tree
        public ActionResult Tree()
        {
            var items = Request.Form["tree"];
            if (null == items)
                items = "";
            ViewData["Tree Items"] = items;
            return View();
        }

        // GET: /Widgets//Store
        public ActionResult Store()
        {
            var shirt = Request.Form["shirt"];
            if (shirt != null)
            {
                string price = "0.00";
                switch (shirt)
                {
                    case "Brown":
                        price = "5.00";
                        break;
                    case "Red":
                        price = "6.00";
                        break;
                    case "Green":
                        price = "7.75";
                        break;
                    case "Black":
                        price = "8.25";
                        break;
                    case "White":
                        price = "9.50";
                        break;
                }
                return Json(price, JsonRequestBehavior.AllowGet);
            }

            ViewData["Color"] = Request.Form["shirtDropdownList"];
            ViewData["Size"] = Request.Form["shirtDropDownListSize"];
            ViewData["Price"] = Request.Form["priceInput"];

            return View();
        }

        // /Widgets/LoginFailed
        public ActionResult LoginFailed()
        {
            return View();
        }

        // /Widgets/Login
        [HttpPost]
        public ActionResult Login()
        {
            ViewData["username"] = Request.Form["username"];
            ViewData["password"] = Request.Form["password"];
            ViewData["rememberme"] = Request.Form["rememberMe"];

            if (Request.Form["username"] != "admin" || Request.Form["password"] != "admin123")
            {
                return RedirectToAction("LoginFailed");
            }

            return View();
        }

        // /Widgets/RegistrationForm
        public ActionResult RegistrationForm(string theme)
        {
            ViewData["Theme"] = theme;
            return View("RegistrationForm");
        }

        // /Widgets/LoginForm
        public ActionResult LoginForm(string theme)
        {
            ViewData["Theme"] = theme;
            return View("LoginForm");
        }



    }
}