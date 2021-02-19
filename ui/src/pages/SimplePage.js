import { Col, Row, Typography } from "antd";

export default function SimplePage({ alternateLink, children, title }) {
  return (
    <Row
      align="middle"
      style={{
        height: "100vh",
      }}
    >
      <Col span={24}>
        <Row justify="center">
          <Col>
            <Typography.Title>{title}</Typography.Title>
          </Col>
        </Row>
        <Row justify="center">
          <Col span={16} md={12} lg={8} xl={6}>
            {children}
          </Col>
        </Row>
        <Row justify="center">
          <Col>{alternateLink}</Col>
        </Row>
      </Col>
    </Row>
  );
}
