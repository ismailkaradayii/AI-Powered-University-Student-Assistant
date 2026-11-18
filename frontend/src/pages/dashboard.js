/**
 * WBS 3.2 - Student Dashboard Page (/pages/dashboard)
 * Displays Weekly Course Schedule, Upcoming Exam Dates, Announcements, and Integrated AI Chatbot Widget.
 * Owner: Rabia Basan (20230147)
 */
import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import Layout from "../components/Layout";
import ChatbotWidget from "../components/ChatbotWidget";
import { apiRequest, getStoredUser } from "../lib/api";

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [courses, setCourses] = useState([]);
  const [exams, setExams] = useState([]);
  const [announcements, setAnnouncements] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedUser = getStoredUser();
    if (!storedUser) {
      router.replace("/pages/login");
      return;
    }
    setUser(storedUser);

    async function fetchDashboardData() {
      try {
        const [coursesData, examsData, announcementsData] = await Promise.all([
          apiRequest("/courses/"),
          apiRequest("/exams/"),
          apiRequest("/announcements/"),
        ]);
        setCourses(coursesData);
        setExams(examsData);
        setAnnouncements(announcementsData);
      } catch (err) {
        console.error("Failed to fetch dashboard data:", err);
      } finally {
        setLoading(false);
      }
    }

    fetchDashboardData();
  }, [router]);

  return (
    <Layout user={user}>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left & Center Column: Announcements, Courses, Exams */}
        <div className="lg:col-span-2 space-y-8">
          {/* Announcements Section */}
          <section className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
            <h2 className="text-lg font-bold text-slate-900 mb-4">
              University Announcements
            </h2>
            {loading ? (
              <p className="text-sm text-slate-500">Loading announcements...</p>
            ) : announcements.length === 0 ? (
              <p className="text-sm text-slate-500">No active announcements.</p>
            ) : (
              <div className="space-y-3">
                {announcements.map((item) => (
                  <div
                    key={item.id}
                    className={`p-4 rounded-lg border ${
                      item.is_important
                        ? "bg-amber-50 border-amber-300"
                        : "bg-slate-50 border-slate-200"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <h3 className="font-semibold text-slate-900 text-sm">
                        {item.title}
                      </h3>
                      {item.is_important && (
                        <span className="bg-amber-600 text-white text-xs px-2 py-0.5 rounded font-medium">
                          Important
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-slate-600 mt-1">{item.content}</p>
                  </div>
                ))}
              </div>
            )}
          </section>

          {/* Weekly Course Schedule */}
          <section className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
            <h2 className="text-lg font-bold text-slate-900 mb-4">
              Weekly Course Schedule
            </h2>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-sm">
                <thead>
                  <tr className="border-b border-slate-200 text-slate-500">
                    <th className="py-2.5 px-3">Code</th>
                    <th className="py-2.5 px-3">Course Name</th>
                    <th className="py-2.5 px-3">Day & Time</th>
                    <th className="py-2.5 px-3">Classroom</th>
                    <th className="py-2.5 px-3">Instructor</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {courses.map((course) => (
                    <tr key={course.id} className="hover:bg-slate-50">
                      <td className="py-3 px-3 font-bold text-red-700">
                        {course.code}
                      </td>
                      <td className="py-3 px-3 font-medium text-slate-800">
                        {course.name}
                      </td>
                      <td className="py-3 px-3 text-slate-600">
                        {course.day} ({course.start_time} - {course.end_time})
                      </td>
                      <td className="py-3 px-3 text-slate-600">
                        {course.classroom}
                      </td>
                      <td className="py-3 px-3 text-slate-600">
                        {course.instructor}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          {/* Exam Timetable */}
          <section className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
            <h2 className="text-lg font-bold text-slate-900 mb-4">
              Exam Timetable
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {exams.map((exam) => (
                <div
                  key={exam.id}
                  className="p-4 rounded-lg border border-slate-200 bg-slate-50"
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-bold text-red-700 text-sm">
                      {exam.course_code}
                    </span>
                    <span className="text-xs font-semibold bg-slate-200 text-slate-800 px-2 py-0.5 rounded">
                      {exam.exam_type}
                    </span>
                  </div>
                  <p className="text-sm font-medium text-slate-800">
                    {exam.course_name}
                  </p>
                  <p className="text-xs text-slate-600 mt-2">
                    Date: <strong>{exam.exam_date}</strong> at{" "}
                    <strong>{exam.exam_time}</strong> &bull; Room:{" "}
                    <strong>{exam.classroom}</strong>
                  </p>
                </div>
              ))}
            </div>
          </section>
        </div>

        {/* Right Column: Live AI Chatbot Assistant (WBS 4.2) */}
        <div className="lg:col-span-1">
          <ChatbotWidget />
        </div>
      </div>
    </Layout>
  );
}
