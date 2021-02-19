import { useQuery } from "react-query";
import axios from "axios";
import { useAuth } from "../../auth";

export default function useGetMessages(roomId) {
  const auth = useAuth();
  return useQuery(["messages", roomId], async () => {
    const response = await axios.get(
      `http://localhost:5000/rooms/${roomId}/messages`,
      {
        headers: {
          Authorization: `Bearer ${auth.username}`,
        },
      }
    );
    return response.data;
  });
}
