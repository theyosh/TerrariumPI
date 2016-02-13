using System;
using System.Collections.Generic;
using System.Data;
using System.Data.Entity;
using System.Linq;
using System.Net;
using System.Web;
using System.Web.Mvc;
using System.Globalization;
using jQWidgetsMVCDemo.Models;

namespace jQWidgetsMVCDemo.Controllers
{
    public class EmployeeController : Controller
    {
        private EmployeesDBEntities db = new EmployeesDBEntities();

        public JsonResult GetEmployees()
        {
            var dbResult = db.Employees.ToList();
            var employees = (from employee in dbResult
                             select new
                             {
                                 employee.FirstName,
                                 employee.LastName,
                                 employee.EmployeeID,
                                 employee.BirthDate,
                                 employee.HireDate,
                                 employee.ManagerID,
                                 employee.Title,
                                 employee.City,
                                 employee.Country,
                                 employee.Address
                             });
            return Json(employees, JsonRequestBehavior.AllowGet);
        }

        // GET: /Employee/
        public ActionResult Index()
        {
            return View(db.Employees.ToList());
        }

        private string BuildQuery(System.Collections.Specialized.NameValueCollection query)
        {
            var result = query.GetValues("filterslength");
            if (result == null)
                return @"SELECT * FROM Employee";

            var filtersCount = int.Parse(query.GetValues("filterslength")[0]);
            var queryString = @"SELECT * FROM Employee ";
            var tmpDataField = "";
            var tmpFilterOperator = "";
            var where = "";
            if (filtersCount > 0)
            {
                where = " WHERE (";
            }
            for (var i = 0; i < filtersCount; i += 1)
            {
                var filterValue = query.GetValues("filtervalue" + i)[0];
                var filterCondition = query.GetValues("filtercondition" + i)[0];
                var filterDataField = query.GetValues("filterdatafield" + i)[0];
                var filterOperator = query.GetValues("filteroperator" + i)[0];
                if (tmpDataField == "")
                {
                    tmpDataField = filterDataField;
                }
                else if (tmpDataField != filterDataField)
                {
                    where += ") AND (";
                }
                else if (tmpDataField == filterDataField)
                {
                    if (tmpFilterOperator == "")
                    {
                        where += " AND ";
                    }
                    else
                    {
                        where += " OR ";
                    }
                }
                // build the "WHERE" clause depending on the filter's condition, value and datafield.
                where += this.GetFilterCondition(filterCondition, filterDataField, filterValue);
                if (i == filtersCount - 1)
                {
                    where += ")";
                }
                tmpFilterOperator = filterOperator;
                tmpDataField = filterDataField;
            }
            queryString += where;
            return queryString;
        }

        private string GetFilterCondition(string filterCondition, string filterDataField, string filterValue)
        {
            switch (filterCondition)
            {
                case "NOT_EMPTY":
                case "NOT_NULL":
                    return " " + filterDataField + " NOT LIKE '" + "" + "'";
                case "EMPTY":
                case "NULL":
                    return " " + filterDataField + " LIKE '" + "" + "'";
                case "CONTAINS_CASE_SENSITIVE":
                    return " " + filterDataField + " LIKE '%" + filterValue + "%'" + " COLLATE SQL_Latin1_General_CP1_CS_AS";
                case "CONTAINS":
                    return " " + filterDataField + " LIKE '%" + filterValue + "%'";
                case "DOES_NOT_CONTAIN_CASE_SENSITIVE":
                    return " " + filterDataField + " NOT LIKE '%" + filterValue + "%'" + " COLLATE SQL_Latin1_General_CP1_CS_AS"; ;
                case "DOES_NOT_CONTAIN":
                    return " " + filterDataField + " NOT LIKE '%" + filterValue + "%'";
                case "EQUAL_CASE_SENSITIVE":
                    return " " + filterDataField + " = '" + filterValue + "'" + " COLLATE SQL_Latin1_General_CP1_CS_AS"; ;
                case "EQUAL":
                    return " " + filterDataField + " = '" + filterValue + "'";
                case "NOT_EQUAL_CASE_SENSITIVE":
                    return " BINARY " + filterDataField + " <> '" + filterValue + "'";
                case "NOT_EQUAL":
                    return " " + filterDataField + " <> '" + filterValue + "'";
                case "GREATER_THAN":
                    return " " + filterDataField + " > '" + filterValue + "'";
                case "LESS_THAN":
                    return " " + filterDataField + " < '" + filterValue + "'";
                case "GREATER_THAN_OR_EQUAL":
                    return " " + filterDataField + " >= '" + filterValue + "'";
                case "LESS_THAN_OR_EQUAL":
                    return " " + filterDataField + " <= '" + filterValue + "'";
                case "STARTS_WITH_CASE_SENSITIVE":
                    return " " + filterDataField + " LIKE '" + filterValue + "%'" + " COLLATE SQL_Latin1_General_CP1_CS_AS"; ;
                case "STARTS_WITH":
                    return " " + filterDataField + " LIKE '" + filterValue + "%'";
                case "ENDS_WITH_CASE_SENSITIVE":
                    return " " + filterDataField + " LIKE '%" + filterValue + "'" + " COLLATE SQL_Latin1_General_CP1_CS_AS"; ;
                case "ENDS_WITH":
                    return " " + filterDataField + " LIKE '%" + filterValue + "'";
            }
            return "";
        }

        public JsonResult GetCurrentEmployees(string sortdatafield, string sortorder, int pagesize, int pagenum)
        {
            var query = Request.QueryString;
            var dbResult = db.Database.SqlQuery<Employee>(this.BuildQuery(query));
            var employees = (from employee in dbResult
                             select new
                             {
                                 employee.FirstName,
                                 employee.LastName,
                                 employee.EmployeeID,
                                 employee.BirthDate,
                                 employee.HireDate,
                                 employee.ManagerID,
                                 employee.Title,
                                 employee.City,
                                 employee.Country,
                                 employee.Address
                             });

            var total = dbResult.Count();
            if (sortorder != null && sortorder != "")
            {
                if (sortorder == "asc")
                {
                    employees = employees.OrderBy(o => o.GetType().GetProperty(sortdatafield).GetValue(o, null));
                }
                else
                {
                    employees = employees.OrderByDescending(o => o.GetType().GetProperty(sortdatafield).GetValue(o, null));
                }
            }
            employees = employees.Skip(pagesize * pagenum).Take(pagesize);
            var result = new
            {
                TotalRows = total,
                Rows = employees
            };
            return Json(result, JsonRequestBehavior.AllowGet);
        }

        // GET: /Employee/Details/5
        public ActionResult Details(int? employeeId)
        {
            if (employeeId == null)
            {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }
            Employee employee = db.Employees.Find(employeeId);
            if (employee == null)
            {
                return HttpNotFound();
            }
            return View(employee);
        }


        [HttpPost]
        public ActionResult Register()
        {
            DateTime maxDate = new DateTime(2015, 1, 1);

            if (Request.Form["birthDateValidate"] != null)
            {
                var birthDateValidate = DateTime.Parse(Request.Form["birthDateValidate"], CultureInfo.CurrentCulture);
                if (birthDateValidate > maxDate)
                {
                    return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
                }
                else
                {
                    return new HttpStatusCodeResult(HttpStatusCode.Accepted);
                }
            }

            if (Request.Form["birthDate"] != null)
            {
                var birthDate = DateTime.Parse(Request.Form["birthDate"], CultureInfo.CurrentCulture);
                if (birthDate > maxDate)
                {
                    return RedirectToAction("RegisterFailed");
                }
            }
            var terms = Request.Form["acceptTerms"];
            if (terms != null)
            {
                if (terms == "false")
                {
                    return RedirectToAction("RegisterFailed");
                }
            }
            Employee employee = new Employee();
            employee.FirstName = Request.Form["FirstName"];
            employee.LastName = Request.Form["LastName"];
            employee.Title = Request.Form["Title"];
            if (Request.Form["birthDate"] != null)
            {
                employee.BirthDate = DateTime.Parse(Request.Form["birthDate"]);
            }
            else employee.BirthDate = new DateTime(1900, 1, 1);

            return View(employee);
        }

        public ActionResult RegisterFailed()
        {
            return View();
        }

        protected override void Dispose(bool disposing)
        {
            if (disposing)
            {
                db.Dispose();
            }
            base.Dispose(disposing);
        }
    }
}
