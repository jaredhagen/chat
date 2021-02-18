import { Col, Divider, Layout, Row, Typography } from "antd";
import { MenuUnfoldOutlined, MenuFoldOutlined } from "@ant-design/icons";
import { useContext, useState } from "react";

import { RoomsMenuContext } from "./RoomsMenu";
import UserMenu from "./UserMenu";

export default function RoomHeader() {
  const { collapsed, selectedRoom, setCollapsed } = useContext(
    RoomsMenuContext
  );

  function toggleCollapsed() {
    setCollapsed(!collapsed);
  }

  return (
    <Layout.Header
      style={{
        background: "#fff",
        borderBottom: "1px solid #ddd",
        paddingLeft: "16px",
      }}
    >
      <Row>
        <Col span={12}>
          <Row gutter={16} align="middle">
            <Col>
              {collapsed ? (
                <MenuUnfoldOutlined
                  style={{
                    fontSize: "16px",
                  }}
                  onClick={toggleCollapsed}
                />
              ) : (
                <MenuFoldOutlined
                  style={{
                    fontSize: "16px",
                  }}
                  onClick={toggleCollapsed}
                />
              )}
            </Col>
            <Col>
              <Typography.Title
                style={{
                  fontSize: "1rem",
                  marginBottom: "5px",
                }}
                level={2}
              >
                {selectedRoom?.name}
              </Typography.Title>
            </Col>
          </Row>
        </Col>
        <Col span={12}>
          <Row type="flex" justify="end" align="middle">
            <Col>
              <Divider type="vertical" style={{ margin: "0 20px" }} />
              <UserMenu />
            </Col>
          </Row>
        </Col>
      </Row>
    </Layout.Header>
  );
}
