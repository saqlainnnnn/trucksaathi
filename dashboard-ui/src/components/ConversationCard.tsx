import { conversation } from "../data/mock";

export default function ConversationCard() {
    return (
        <div className="flex h-72 flex-col gap-3 overflow-y-auto rounded-lg bg-zinc-950 p-4">
            {conversation.map((message, index) => (
                <div
                    key={index}
                    className={`max-w-[80%] rounded-2xl px-4 py-3 shadow ${
                        message.role === "user"
                            ? "ml-auto rounded-br-md bg-blue-600 text-white"
                            : "mr-auto rounded-bl-md bg-zinc-800 text-zinc-100"
                    }`}
                >
                    <p className="text-sm leading-relaxed">
                        {message.text}
                    </p>
                </div>
            ))}
        </div>
    );
}