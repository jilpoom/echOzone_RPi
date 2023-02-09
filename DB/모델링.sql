팀명 : echOzone
팀원 : 정정용, 이진옥, 국현지, 최정운, 박지형
주제 : 세척 여부 판단 머신러닝 모델을 이용한 재활용 세척 및 수거함
일시 : 2022.05.16 09:00-13:00

멘토 김광진 router128@hanmail.net

> 모델링 주소 
URL : https://aquerytool.com/aquerymain/index/?rurl=48edde18-35a2-4aef-bbe5-d83b0d31675a&
Password : i241ux


타입사전/단어사전/용어사전을 만들자

타입 사전 : 오라클 여러개의 타입중에서 프로젝트에 필요한 타입을 골라서 미리 정리해 둠
단어 사전 : 요구사항 정의성의 명사를 찾아서 사전으로 만듦.
용어 사전 : 단어 사전에 있는 단어를 조합해서 필요한 용어를 만든다.(회원 + 아이디 = 회원 아이디)


> MySQL 서버 구축 정보 

host : localhost 
db   : echozone_db
user : echozone_user
pass : 1234


use mysql;

--(1) DB 생성
--(2) USER 생성
--(3) 권한 부여
--(4) 권한 반영


--(1) DB 생성
create database echozone_db;

--(2) USER 생성
create user echozone_user@localhost identified by '1234';

--(3) 권한 부여(INSERT/UPDATE/DELETE/SELECT/CREATE TABLE... 권한 : PRIVILEGE)
GRANT ALL PRIVILEGES ON echozone_db.* TO echozone_user@localhost;

--(4) 권한 반영
FLUSH PRIVILEGES;





MySQL text 타입 : 

. int            ... 32 bit 정수 [-2147483648~-,1 0~2147483647]   대충 42억 x개 
. int unsigned   ... 32 bit 정수 [0~2147483647 + 2147483648]      대충 42억 x개 
. tinytext/text/mediumtext/longtext

text : 2^16-1 크기 : 65535 bytes(utf-8 모드에서 한글 18,144글자 정도)


> 점포별 마일리지 합계 : VIEW로 만들면 된다. 


> MySQL DBMS(Database Management System) : MySQL Workbench / Oracle Sql Developer 



-- 테이블 순서는 관계를 고려하여 한 번에 실행해도 에러가 발생하지 않게 정렬되었습니다.
use echozone_db;
-- product_info Table Create SQL
-- 테이블 순서는 관계를 고려하여 한 번에 실행해도 에러가 발생하지 않게 정렬되었습니다.
use echozone_db;
-- product_info Table Create SQL
-- 테이블 순서는 관계를 고려하여 한 번에 실행해도 에러가 발생하지 않게 정렬되었습니다.

-- product_info Table Create SQL
CREATE TABLE product_info
(
    `product_seq`     INT UNSIGNED    NOT NULL    AUTO_INCREMENT COMMENT '제품 고유번호', 
    `product_cap`     VARCHAR(25)     NOT NULL    COMMENT '제품 용량', 
    `manufacture_dt`  DATETIME        NOT NULL    COMMENT '제조 일자', 
    `shop_id`         VARCHAR(25)     NOT NULL    COMMENT '점포 아이디', 
     PRIMARY KEY (product_seq)
);


-- user_info Table Create SQL
CREATE TABLE user_info
(
    `user_id`        VARCHAR(25)     NOT NULL    COMMENT '사용자 아이디', 
    `user_pw`        VARCHAR(25)     NOT NULL    COMMENT '사용자 비밀번호', 
    `user_seq`       INT UNSIGNED    NOT NULL    COMMENT '사용자 고유번호', 
    `user_type`      CHAR(1)         NOT NULL    COMMENT '사용자 유형', 
    `user_phone`     VARCHAR(25)     NOT NULL    COMMENT '사용자 휴대폰번호', 
    `user_address`   VARCHAR(300)    NOT NULL    COMMENT '사용자 주소', 
    `user_nm`        VARCHAR(25)     NOT NULL    COMMENT '사용자 명', 
    `user_joindate`  DATETIME        NOT NULL    DEFAULT NOW() COMMENT '사용자 가입일자', 
     PRIMARY KEY (user_id)
);

ALTER TABLE user_info COMMENT '사용자 정보 테이블';

CREATE UNIQUE INDEX UQ_user_info_1
    ON user_info(user_phone);


-- shop_info Table Create SQL
CREATE TABLE shop_info
(
    `shop_id`       VARCHAR(25)     NOT NULL    COMMENT '점포 아이디', 
    `shop_pw`       VARCHAR(25)     NOT NULL    COMMENT '점포 비밀번호', 
    `shop_seq`      INT UNSIGNED    NOT NULL    COMMENT '점포 고유번호', 
    `com_resid`     VARCHAR(25)     NOT NULL    COMMENT '사업자 등록번호', 
    `product_seq`   INT UNSIGNED    NOT NULL    COMMENT '제품 고유번호', 
    `inst_dt`       DATETIME        NOT NULL    DEFAULT NOW() COMMENT '설치 일자', 
    `shop_nm`       VARCHAR(25)     NOT NULL    COMMENT '점포 명', 
    `shop_address`  VARCHAR(300)    NOT NULL    COMMENT '점포 주소', 
     PRIMARY KEY (shop_id)
);

ALTER TABLE shop_info COMMENT '사업주 정보 테이블';

ALTER TABLE shop_info
    ADD CONSTRAINT FK_shop_info_product_seq_product_info_product_seq FOREIGN KEY (product_seq)
        REFERENCES product_info (product_seq) ON DELETE RESTRICT ON UPDATE RESTRICT;


-- user_mileage_info Table Create SQL
CREATE TABLE user_mileage_info
(
    `mileage_seq`   INT UNSIGNED    NOT NULL    COMMENT '마일리지 고유번호', 
    `user_id`       VARCHAR(25)     NOT NULL    COMMENT '사용자 아이디', 
    `shop_id`       VARCHAR(25)     NOT NULL    COMMENT '점포 아이디', 
    `user_mileage`  INT             NOT NULL    COMMENT '사용자 마일리지', 
    `mileage_dt`    DATETIME        NOT NULL    DEFAULT NOW() COMMENT '마일리지 일자', 
     PRIMARY KEY (mileage_seq)
);

ALTER TABLE user_mileage_info COMMENT '사용자의 마일리지 적립 정보';

ALTER TABLE user_mileage_info
    ADD CONSTRAINT FK_user_mileage_info_shop_id_shop_info_shop_id FOREIGN KEY (shop_id)
        REFERENCES shop_info (shop_id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE user_mileage_info
    ADD CONSTRAINT FK_user_mileage_info_user_id_user_info_user_id FOREIGN KEY (user_id)
        REFERENCES user_info (user_id) ON DELETE RESTRICT ON UPDATE RESTRICT;


-- t1 Table Create SQL
CREATE TABLE t1
(
    `user_id`        VARCHAR(25)     NOT NULL    COMMENT '사용자 아이디', 
    `user_pw`        VARCHAR(25)     NOT NULL    COMMENT '사용자 비밀번호', 
    `user_seq`       INT UNSIGNED    NOT NULL    COMMENT '사용자 고유번호', 
    `user_type`      CHAR(1)         NOT NULL    COMMENT '사용자 유형', 
    `user_phone`     VARCHAR(25)     NOT NULL    COMMENT '사용자 휴대폰번호', 
    `user_address`   VARCHAR(300)    NOT NULL    COMMENT '사용자 주소', 
    `user_nm`        VARCHAR(25)     NOT NULL    COMMENT '사용자 명', 
    `user_joindate`  DATETIME        NOT NULL    DEFAULT NOW() COMMENT '사용자 가입일자', 
    `product_seq`    INT UNSIGNED    NOT NULL    COMMENT '제품 고유번호', 
     PRIMARY KEY (user_id)
);

ALTER TABLE t1 COMMENT '사용자 정보 테이블';


-- t2 Table Create SQL
CREATE TABLE t2
(
    `user_id`        VARCHAR(25)     NOT NULL    COMMENT '사용자 아이디', 
    `user_pw`        VARCHAR(25)     NOT NULL    COMMENT '사용자 비밀번호', 
    `user_seq`       INT UNSIGNED    NOT NULL    COMMENT '사용자 고유번호', 
    `user_type`      CHAR(1)         NOT NULL    COMMENT '사용자 유형', 
    `user_phone`     VARCHAR(25)     NOT NULL    COMMENT '사용자 휴대폰번호', 
    `user_address`   VARCHAR(300)    NOT NULL    COMMENT '사용자 주소', 
    `user_nm`        VARCHAR(25)     NOT NULL    COMMENT '사용자 명', 
    `user_joindate`  DATETIME        NOT NULL    DEFAULT NOW() COMMENT '사용자 가입일자', 
     PRIMARY KEY (user_id)
);

ALTER TABLE t2 COMMENT '사용자 정보 테이블';


--------------------------------------------------------
> 그냥 상점별 마일리지 리스트 : 뷰(View)로 해결함.
)

> 개인별 마일리지/ 개별 상점 마일리지 구하기
. function(함수)를 만든다.   get_mileage(매개변수 p_user_id varchar(30))

CREATE FUNTION get_mileage
RETURNS int 
...
....


SELECT mileage_seq, user_id, shop_id, user_mileage, mileage_dt
FROM user_mileage_info
WHERE user_id = 'abcd';


SELECT sum(user_mileage)
FROM user_mileage_info
WHERE user_id = 'abcd';

자바에서 mysql 함수(function)의 결과값을 가져오기 
. Connection 
. CallabeStatement를 사용해서 함수를 호출해서 결과값을 받음. 

CallabeStatement를  cstmt = null;
String fn_call = "{? = call get_mileage(?)}";
cstmt = conn.getPrepareCall(fn_call)
cstmt.registerOutParameter(1, OracleTypes.CURSOR);
cstmt.setString(2, 'tom');
ResultSet rs = cstmt.executeQuery();

// ResultSet rs = (ResultSet) cstmt.getObject(1);

while(rs.next())
{
    int mileage = rs.getInt("mileage");
    
}

> 상점별 마일리지 구하기


> 사용자 아이디로 사용자 정보 조회하기

>

