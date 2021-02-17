import { useQuery } from "react-query";
import axios from "axios";

export default function useRooms() {
  return useQuery("rooms", () =>
    axios
      .get("http://localhost:5000/rooms", {
        headers: {
          Authorization: "Bearer default",
        },
      })
      .then((res) => res.data)
  );
}
