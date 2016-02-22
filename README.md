# GetMeThat
GetMeThat is a web portal for employees to request trivial services (like Tea, Coffee) to errand boys, in an office/ organization. Each of the employees and errand boys have their own account on the portal.
There is also an admin account, who can add/remove services and accounts of employees and errand boys.

## Working
* Admin logs in with his account, and can add services and Employees/Errand Boys to the database.
(When admin adds a user, the username/password of that user becomes his full name (spaces removed), eg if Name="Mark Charles", his username, password would be: MarkCharles)

* Employees can log in with their account and request services and view their pending services. The errand boy which has the least jobs assigned, get this new job.

* Errand boys can view their jobs assigned to them, and by whom. After granting the job, they click on the 'check' button of that job.

* After a job is granted by the errand boy, the employee can now 'check' and accept that job. Thus a job process is complete.

* The assigining, granting and accepting of jobs change in real time.

#### Sample accounts to test the site:
| Role  | Username  | Password  |
|---|---|---|
| Admin  | bhrigu | bhrigu  |
| Employee  | ashish  | ashish  |
| Errand Boy | anshuman  | anshuman  |
| Errand Boy | puneet | puneet |

(You can visit /admin to tweak around the entries in the database for testing purposes)
