import { useMutation, useQueryClient } from "react-query";
import axios from "axios";
import { useAuth } from "../../auth";

// See: https://react-query.tanstack.com/guides/optimistic-updates
export default function usePostRoom() {
  const queryClient = useQueryClient();
  const auth = useAuth();
  const roomsQueryKey = ["rooms"];
  return useMutation(
    async (newRoom) => {
      const response = await axios.post(
        `http://localhost:5000/rooms`,
        newRoom,
        {
          headers: {
            Authorization: `Bearer ${auth.username}`,
          },
        }
      );
      return response.data;
    },
    {
      onMutate: async (newRoom) => {
        await queryClient.cancelQueries(roomsQueryKey);
        const previousRooms = queryClient.getQueryData(roomsQueryKey);
        queryClient.setQueryData(roomsQueryKey, (old) => {
          return {
            messages: [
              ...old.rooms,
              {
                id: newRoom.name,
                ...newRoom,
              },
            ],
          };
        });

        return { previousRooms };
      },
      onError: (err, newRoom, context) => {
        queryClient.setQueryData(roomsQueryKey, context.previousRooms);
      },
      onSettled: () => {
        queryClient.invalidateQueries(roomsQueryKey);
      },
    }
  );
}
