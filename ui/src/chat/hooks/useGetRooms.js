import { useQuery } from "react-query";
import axios from "axios";
import { useAuth } from "../../auth";

// Consider the room data stale after 10 seconds
const STALE_TIME = 10000;

export default function useGetRooms() {
  const auth = useAuth();
  return useQuery(
    "rooms",
    async () => {
      const response = await axios.get(
        "http://localhost:5000/rooms",
        {
          headers: {
            Authorization: `Bearer ${auth.username}`,
          },
        },
        {
          staleTime: STALE_TIME,
        }
      );
      return response.data;
    },
    {
      retry: false,
      onError: (error, other, other2, other3) => {
        if (error.response.status == 401) {
          auth.logOut();
        }
      },
    }
  );
}
