import { useQuery } from "react-query";
import axios from "axios";
import { useAuth } from "../../auth";

export default function useGetRooms() {
  const auth = useAuth();
  return useQuery("rooms", async () => {
    const response = await axios.get("http://localhost:5000/rooms", {
      headers: {
        Authorization: `Bearer ${auth.user.token}`,
      },
    });
    return response.data;
  });
}
