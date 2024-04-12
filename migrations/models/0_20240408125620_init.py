from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `org` (
    `orgId` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '机构ID',
    `orgName` VARCHAR(64) NOT NULL  COMMENT '机构名',
    `orgType` INT NOT NULL  COMMENT '机构类型'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `user` (
    `userId` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    `username` VARCHAR(16) NOT NULL  COMMENT '用户名',
    `photoUrl` VARCHAR(128) NOT NULL  COMMENT '图片路径',
    `createTime` VARCHAR(64) NOT NULL  COMMENT '创建时间',
    `orgId_id` BIGINT NOT NULL,
    CONSTRAINT `fk_user_org_de743fce` FOREIGN KEY (`orgId_id`) REFERENCES `org` (`orgId`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
