import { useQuery } from "react-query";
import axios from "axios";

export default function useMessages(roomId) {
  return useQuery("messages", () =>
    axios
      .get(`http://localhost:5000/rooms/${roomId}/messages`, {
        headers: {
          Authorization: "Bearer default",
        },
      })
      .then((res) => res.data)
  );
}
