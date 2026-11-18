/**
 * WBS 2.2 & 4.2 - Admin Panel Interface (/pages/admin)
 * Covers Test Case TC-05 (Admin Panel Data Update: New Announcement & Exam Date Update)
 * Owner: Fatih Yazıcı (20211046)
 */
import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import Layout from "../components/Layout";
import { apiRequest, getStoredUser } from "../lib/api";

export default function AdminPage() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [exams, setExams] = useState([]);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [isImportant, setIsImportant] = useState(true);
  const [selectedExamId, setSelectedExamId] = useState("");
  const [newExamDate, setNewExamDate] = useState("");
  const [newExamTime, setNewExamTime] = useState("");
  const [statusMsg, setStatusMsg] = useState("");

  useEffect(() => {
    const storedUser = getStoredUser();
    if (!storedUser) {
      router.replace("/pages/login");
      return;
    }
    setUser(storedUser);
    loadExams();
  }, [router]);

  const loadExams = async () => {
    try {
      const data = await apiRequest("/exams/");
      setExams(data);
      if (data.length > 0) {
        setSelectedExamId(String(data[0].id));
        setNewExamDate(data[0].exam_date);
        setNewExamTime(data[0].exam_time);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleCreateAnnouncement = async (e) => {
    e.preventDefault();
    setStatusMsg("");
    try {
      await apiRequest("/announcements/", {
        method: "POST",
        body: JSON.stringify({
          title,
          content,
          is_important: isImportant,
        }),
      });
      setTitle("");
      setContent("");
      setStatusMsg("Announcement saved to SQLite database immediately (TC-05).");
    } catch (err) {
      setStatusMsg(`Error: ${err.message}`);
    }
  };

  const handleUpdateExamDate = async (e) => {
    e.preventDefault();
    setStatusMsg("");
    const target = exams.find((ex) => String(ex.id) === String(selectedExamId));
    if (!target) return;

    try {
      await apiRequest(`/exams/${target.id}/`, {
        method: "PUT",
        body: JSON.stringify({
          course: target.course,
          exam_type: target.exam_type,
          exam_date: newExamDate,
          exam_time: newExamTime,
          classroom: target.classroom,
          notes: target.notes,
        }),
      });
      await loadExams();
      setStatusMsg(
        `Exam date for ${target.course_code} (${target.exam_type}) updated in SQLite immediately (TC-05).`
      );
    } catch (err) {
      setStatusMsg(`Error: ${err.message}`);
    }
  };

  return (
    <Layout user={user}>
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h1 className="text-xl font-bold text-slate-900">
            Admin Management Panel (TC-05)
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Publish announcements and update course exam dates in real time.
          </p>

          {statusMsg && (
            <div className="mt-4 p-3 rounded-lg bg-emerald-50 border border-emerald-300 text-emerald-800 text-sm font-medium">
              {statusMsg}
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Publish New Announcement */}
          <form
            onSubmit={handleCreateAnnouncement}
            className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 space-y-4"
          >
            <h2 className="text-base font-bold text-slate-900">
              Publish New Announcement
            </h2>
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">
                Announcement Title
              </label>
              <input
                type="text"
                required
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g. SWE488 Exam Room Updated"
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">
                Content
              </label>
              <textarea
                rows={3}
                required
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Enter official announcement details..."
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm"
              />
            </div>
            <label className="flex items-center space-x-2 text-sm text-slate-700">
              <input
                type="checkbox"
                checked={isImportant}
                onChange={(e) => setIsImportant(e.target.checked)}
              />
              <span>Mark as Important Announcement</span>
            </label>
            <button
              type="submit"
              className="w-full bg-slate-900 hover:bg-slate-800 text-white font-semibold py-2 rounded-lg text-sm"
            >
              Save Announcement
            </button>
          </form>

          {/* Update Exam Date */}
          <form
            onSubmit={handleUpdateExamDate}
            className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 space-y-4"
          >
            <h2 className="text-base font-bold text-slate-900">
              Update Course Exam Date
            </h2>
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">
                Select Exam
              </label>
              <select
                value={selectedExamId}
                onChange={(e) => {
                  setSelectedExamId(e.target.value);
                  const found = exams.find(
                    (ex) => String(ex.id) === String(e.target.value)
                  );
                  if (found) {
                    setNewExamDate(found.exam_date);
                    setNewExamTime(found.exam_time);
                  }
                }}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm"
              >
                {exams.map((ex) => (
                  <option key={ex.id} value={ex.id}>
                    {ex.course_code} - {ex.exam_type} ({ex.exam_date})
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">
                New Exam Date
              </label>
              <input
                type="date"
                required
                value={newExamDate}
                onChange={(e) => setNewExamDate(e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">
                New Exam Time
              </label>
              <input
                type="text"
                required
                value={newExamTime}
                onChange={(e) => setNewExamTime(e.target.value)}
                placeholder="10:00"
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm"
              />
            </div>
            <button
              type="submit"
              className="w-full bg-red-700 hover:bg-red-800 text-white font-semibold py-2 rounded-lg text-sm"
            >
              Update Exam Schedule
            </button>
          </form>
        </div>
      </div>
    </Layout>
  );
}
