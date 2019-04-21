DROP TABLE IF EXISTS `caselist`;
CREATE TABLE IF NOT EXISTS `caselist` (
  `id` int(16) NOT NULL AUTO_INCREMENT,
  `user_id` int(16) NOT NULL,
  `user_name` varchar(24) NOT NULL,
  `title` varchar(1024) NOT NULL,
  `server` varchar(256) NOT NULL,
  `mock_status` int(2) NOT 0 COMMENT '是否已经录制接口',
  `status` int(2) NOT 0 COMMENT '测试结果',
  `reset_status` int(2) NOT 0 COMMENT '重置标志',
  `script_name` varchar(256) NOT NULL,
  `script_name_old` varchar(256) NOT NULL,
  `sprint` int(5) NOT NULL,
  `script` longtext,
  `create_time` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

insert into caselist(id, user_id, user_name, title, server, mock_status, status, reset_status, script_name, script_name_old, script, create_time) values(1, 1, 'admin', '商城直接购买商品，白条支付', 'QDD', '0', '0', '0', 'TC_QDD_baitiao001', 'TC_QDD_baitiao001', 97, '', 1549639959), (2, 1, 'admin', '商城直接购买商品，挂账支付', 'QDD', '1', '1', '1', 'TC_QDD_guazhang001', 'TC_QDD_guazhang001', 97, '', 1549640336), (3, 1, 'admin', '商城直接购买商品，微信支付', 'QDD', '1', '0', '0', 'TC_QDD_weichat001', 'TC_QDD_weichat001', 97, '', 1549640355);

DROP TABLE IF EXISTS `base_user`;
CREATE TABLE `base_user` (
  `id` int(16) NOT NULL AUTO_INCREMENT,
  `username` varchar(24) NOT NULL,
  `password` varchar(24) NOT NULL,
  `uname` varchar(24) NOT NULL,
  `userver` varchar(24) NOT NULL,
   `user_status` int(2) DEFAULT 1 COMMENT '用户状态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

insert into base_user values(1, 'admin', 'admin', '管理员', 'ALL', 1);
insert into base_user values(2, 'ban', '123456', 'ban', 'ALL', 1);
insert into base_user values(3, 'yuefan.huang', '123456', '黄岳樊', 'QDD', 1);
insert into base_user values(4, 'xinpan.li', '123456', '李新盼', 'SOS', 1);

