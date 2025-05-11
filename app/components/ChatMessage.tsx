import ReactMarkdown from "react-markdown";

export default function ChatMessage({
  message,
}: {
  message: { role: string; content: string };
}) {
  return (
    <div
      className={`p-4 rounded-lg ${
        message.role === "user" ? "bg-blue-50 ml-auto" : "bg-gray-50 mr-auto"
      } max-w-[75%]`}
    >
      <p className="font-semibold mb-2 text-gray-700">
        {message.role === "user" ? "You" : "DefiPT"}
      </p>
      <div className="prose prose-sm max-w-none">
        <ReactMarkdown>{message.content}</ReactMarkdown>
      </div>
    </div>
  );
}
