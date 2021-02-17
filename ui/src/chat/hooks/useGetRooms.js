import { useQuery } from "react-query";
import axios from "axios";

export default function useGetRooms() {
  return useQuery("rooms", async () => {
    const response = await axios.get("http://localhost:5000/rooms", {
      headers: {
        Authorization: "Bearer default",
      },
    });
    return response.data;
  });
}
