import { useQuery } from "react-query";
import axios from "axios";
import { useAuth } from "./useAuth";

// Consider the room data stale after 10 seconds
const STALE_TIME = 10000;

export default function useGetRooms() {
  const auth = useAuth();
  return useQuery(
    "rooms",
    async () => {
      const response = await axios.get(
        `${process.env.REACT_APP_CHAT_API_ENDPOINT}/rooms`,
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
