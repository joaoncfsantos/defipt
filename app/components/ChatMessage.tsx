export default function ChatMessage({
  message,
}: {
  message: { role: string; content: string };
}) {
  return (
    <p className="text-gray-800">
      {message.role === "user" ? "User: " : "Bot: "}
      {message.content}
    </p>
  );
}
