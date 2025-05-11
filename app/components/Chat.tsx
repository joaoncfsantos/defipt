import ChatMessage from "./ChatMessage";

export default function Chat({
  chatHistory,
}: {
  chatHistory: { role: string; content: string }[];
}) {
  return (
    <div className="flex flex-col gap-2 w-full max-w-screen-xl mx-auto">
      {chatHistory.map((message, index) => (
        <ChatMessage key={index} message={message} />
      ))}
    </div>
  );
}
