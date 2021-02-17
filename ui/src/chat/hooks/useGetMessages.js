import { useQuery } from "react-query";
import axios from "axios";

export default function useGetMessages(roomId) {
  return useQuery(["messages", roomId], async () => {
    const response = await axios.get(
      `http://localhost:5000/rooms/${roomId}/messages`,
      {
        headers: {
          Authorization: "Bearer default",
        },
      }
    );
    return response.data;
  });
}
