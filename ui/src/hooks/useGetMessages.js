import { useQuery } from "react-query";
import axios from "axios";
import { useAuth } from "./useAuth";

// Consider the message data stale after 2 seconds
const STALE_TIME = 2000;

export default function useGetMessages(roomId) {
  const auth = useAuth();
  return useQuery(
    ["messages", roomId],
    async () => {
      const response = await axios.get(
        `${process.env.REACT_APP_CHAT_API_ENDPOINT}/rooms/${roomId}/messages`,
        {
          headers: {
            Authorization: `Bearer ${auth.username}`,
          },
        }
      );
      return response.data;
    },
    {
      retry: false,
      staleTime: STALE_TIME,
      onError: (error) => {
        if (error?.response?.status === 401) {
          auth.logOut();
        }
      },
    }
  );
}
