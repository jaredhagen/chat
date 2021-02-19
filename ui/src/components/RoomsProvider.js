import { createContext } from "react";

import { Spin } from "antd";
import { Redirect } from "react-router-dom";

import { useGetRooms } from "../hooks";

const RoomsContext = createContext();

function RoomsProvider({ children }) {
  const { isLoading, error, data } = useGetRooms();

  if (isLoading) return <Spin />;

  if (error) return <Redirect to="/login" />;

  return <RoomsContext.Provider value={data}>{children}</RoomsContext.Provider>;
}

export { RoomsContext, RoomsProvider };
