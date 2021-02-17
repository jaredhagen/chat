import { useQuery } from "react-query";

import Message from "./Message";

const messages = [
  { author: "gandalf", content: "hello" },
  { author: "frodo", content: "howdy" },
  { author: "sam", content: "goodbye" },
  { author: "aragorn", content: "see ya" },
];

function Messages() {
  const result = useQuery("todos", () =>
    fetch("http://localhost:5000/rooms/id/messages")
  );

  return (
    <div>
      {messages.map((message) => (
        <Message author={message.author} content={message.content}></Message>
      ))}
    </div>
  );
}

export default Messages;
