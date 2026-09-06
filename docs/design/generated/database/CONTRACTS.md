# 移行・索引・DB内部契約

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

全移行をPostgreSQL文法で解析する。関数本体はソースとして示し、DB内実行の受入は結合テスト結果で確認する。

| 定義元 | SQL構文種別 |
|---|---|
| database/migrations/001_user_state.sql:statement-1 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-1 | CreateExtensionStmt |
| database/migrations/002_relational_schema.sql:statement-2 | CreateExtensionStmt |
| database/migrations/002_relational_schema.sql:statement-3 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-13 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-20 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-30 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-40 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-47 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-57 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-69 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-79 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-88 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-101 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-111 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-118 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-126 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-134 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-141 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-152 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-162 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-172 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-178 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-186 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-200 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-206 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-218 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-225 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-245 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-255 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-268 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-281 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-290 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-301 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-308 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-317 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-325 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-334 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-347 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-355 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-365 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-377 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-383 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-390 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-400 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-411 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-421 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-430 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-439 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-447 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-454 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-462 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-471 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-479 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-488 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-498 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-507 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-518 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-531 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-540 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-549 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-560 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-571 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-582 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-592 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-601 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-611 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-618 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-626 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-636 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-648 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-660 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-674 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-683 | CreateStmt |
| database/migrations/002_relational_schema.sql:statement-699 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-700 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-701 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-702 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-703 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-704 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-705 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-706 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-707 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-708 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-709 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-710 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-711 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-712 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-713 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-714 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-715 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-716 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-717 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-718 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-719 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-720 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-721 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-722 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-723 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-724 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-725 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-726 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-727 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-728 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-729 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-730 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-731 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-732 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-733 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-734 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-735 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-736 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-737 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-738 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-739 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-740 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-741 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-742 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-743 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-744 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-745 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-746 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-747 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-748 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-749 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-750 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-751 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-752 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-753 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-754 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-755 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-756 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-757 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-758 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-759 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-760 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-761 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-762 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-763 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-764 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-765 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-766 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-767 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-768 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-769 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-770 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-771 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-772 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-773 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-774 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-775 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-776 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-777 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-778 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-779 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-780 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-781 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-782 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-783 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-784 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-785 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-786 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-787 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-788 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-789 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-790 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-791 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-792 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-793 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-794 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-795 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-796 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-797 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-798 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-799 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-800 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-801 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-802 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-803 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-804 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-805 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-806 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-807 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-808 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-809 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-810 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-811 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-812 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-813 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-814 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-815 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-816 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-817 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-818 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-819 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-820 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-821 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-822 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-823 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-824 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-825 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-826 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-827 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-828 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-829 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-830 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-831 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-832 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-833 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-834 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-835 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-836 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-837 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-838 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-839 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-840 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-841 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-842 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-843 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-844 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-845 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-846 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-847 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-848 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-849 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-850 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-851 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-852 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-853 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-854 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-855 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-856 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-857 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-858 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-859 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-860 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-861 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-862 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-863 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-864 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-865 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-866 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-867 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-868 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-869 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-870 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-871 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-872 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-873 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-874 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-875 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-876 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-877 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-878 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-879 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-880 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-881 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-882 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-883 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-884 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-885 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-886 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-887 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-888 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-889 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-890 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-891 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-892 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-893 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-894 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-895 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-896 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-897 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-898 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-899 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-900 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-901 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-902 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-903 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-904 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-905 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-906 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-907 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-908 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-909 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-910 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-911 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-912 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-913 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-914 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-915 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-916 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-917 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-918 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-919 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-920 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-921 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-922 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-923 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-924 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-925 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-926 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-927 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-928 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-929 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-930 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-931 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-932 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-933 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-934 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-935 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-936 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-937 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-938 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-939 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-940 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-941 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-942 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-943 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-944 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-945 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-946 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-947 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-948 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-949 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-950 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-951 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-952 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-953 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-954 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-955 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-956 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-957 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-958 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-959 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-960 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-961 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-962 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-963 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-964 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-965 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-966 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-967 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-968 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-969 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-970 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-971 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-972 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-973 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-974 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-975 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-976 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-977 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-978 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-979 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-980 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-981 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-982 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-983 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-984 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-985 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-986 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-987 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-988 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-989 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-990 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-991 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-992 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-993 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-994 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-995 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-996 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-997 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-998 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-999 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-1000 | IndexStmt |
| database/migrations/002_relational_schema.sql:statement-1001 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1002 | CreateFunctionStmt |
| database/migrations/002_relational_schema.sql:statement-1003 | CreateFunctionStmt |
| database/migrations/002_relational_schema.sql:statement-1004 | CreateFunctionStmt |
| database/migrations/002_relational_schema.sql:statement-1005 | CreateFunctionStmt |
| database/migrations/002_relational_schema.sql:statement-1006 | CreateFunctionStmt |
| database/migrations/002_relational_schema.sql:statement-1007 | CreateFunctionStmt |
| database/migrations/002_relational_schema.sql:statement-1008 | CreateFunctionStmt |
| database/migrations/002_relational_schema.sql:statement-1009 | CreateFunctionStmt |
| database/migrations/002_relational_schema.sql:statement-1010 | CreateFunctionStmt |
| database/migrations/002_relational_schema.sql:statement-1011 | CreateFunctionStmt |
| database/migrations/002_relational_schema.sql:statement-1012 | CreateFunctionStmt |
| database/migrations/002_relational_schema.sql:statement-1013 | CreateFunctionStmt |
| database/migrations/002_relational_schema.sql:statement-1014 | CreateFunctionStmt |
| database/migrations/002_relational_schema.sql:statement-1015 | CreateFunctionStmt |
| database/migrations/002_relational_schema.sql:statement-1016 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1017 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1018 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1019 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1020 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1021 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1022 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1023 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1024 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1025 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1026 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1027 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1028 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1029 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1030 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1031 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1032 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1033 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1034 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1035 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1036 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1037 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1038 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1039 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1040 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1041 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1042 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1043 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1044 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1045 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1046 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1047 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1048 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1049 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1050 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1051 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1052 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1053 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1054 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1055 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1056 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1057 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1058 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1059 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1060 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1061 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1062 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1063 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1064 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1065 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1066 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1067 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1068 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1069 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1070 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1071 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1072 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1073 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1074 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1075 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1076 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1077 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1078 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1079 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1080 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1081 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1082 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1083 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1084 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1085 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1086 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1087 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1088 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1089 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1090 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1091 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1092 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1093 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1094 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1095 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1096 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1097 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1098 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1099 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1100 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1101 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1102 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1103 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1104 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1105 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1106 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1107 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1108 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1109 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1110 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1111 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1112 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1113 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1114 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1115 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1116 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1117 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1118 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1119 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1120 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1121 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1122 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1123 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1124 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1125 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1126 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1127 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1128 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1129 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1130 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1131 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1132 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1133 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1134 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1135 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1136 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1137 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1138 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1139 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1140 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1141 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1142 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1143 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1144 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1145 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1146 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1147 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1148 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1149 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1150 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1151 | CreatePolicyStmt |
| database/migrations/002_relational_schema.sql:statement-1152 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1153 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1154 | CreatePolicyStmt |
| database/migrations/002_relational_schema.sql:statement-1155 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1156 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1157 | CreatePolicyStmt |
| database/migrations/002_relational_schema.sql:statement-1158 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1159 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1160 | CreatePolicyStmt |
| database/migrations/002_relational_schema.sql:statement-1161 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1162 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1163 | CreatePolicyStmt |
| database/migrations/002_relational_schema.sql:statement-1164 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1165 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1166 | CreatePolicyStmt |
| database/migrations/002_relational_schema.sql:statement-1167 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1168 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1169 | CreatePolicyStmt |
| database/migrations/002_relational_schema.sql:statement-1170 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1171 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1172 | CreatePolicyStmt |
| database/migrations/002_relational_schema.sql:statement-1173 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1174 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1175 | CreatePolicyStmt |
| database/migrations/002_relational_schema.sql:statement-1176 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1177 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1178 | CreatePolicyStmt |
| database/migrations/002_relational_schema.sql:statement-1179 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1180 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1181 | CreatePolicyStmt |
| database/migrations/002_relational_schema.sql:statement-1182 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1183 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1184 | CreatePolicyStmt |
| database/migrations/002_relational_schema.sql:statement-1185 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1186 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1187 | CreatePolicyStmt |
| database/migrations/002_relational_schema.sql:statement-1188 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1189 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1190 | CreatePolicyStmt |
| database/migrations/002_relational_schema.sql:statement-1191 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1192 | AlterTableStmt |
| database/migrations/002_relational_schema.sql:statement-1193 | CreatePolicyStmt |
| database/migrations/002_relational_schema.sql:statement-1194 | CreateFunctionStmt |
| database/migrations/002_relational_schema.sql:statement-1195 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1196 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1197 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1198 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1199 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1200 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1201 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1202 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1203 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1204 | CreateTrigStmt |
| database/migrations/002_relational_schema.sql:statement-1205 | CreateTrigStmt |
| database/migrations/003_service_operations.sql:statement-1 | CreateStmt |
| database/migrations/003_service_operations.sql:statement-12 | CreateStmt |
| database/migrations/003_service_operations.sql:statement-25 | CreateStmt |
| database/migrations/003_service_operations.sql:statement-31 | CreateStmt |
| database/migrations/003_service_operations.sql:statement-37 | CreateStmt |
| database/migrations/003_service_operations.sql:statement-43 | CreateStmt |
| database/migrations/003_service_operations.sql:statement-52 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-54 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-56 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-58 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-60 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-62 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-64 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-66 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-68 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-70 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-72 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-74 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-76 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-78 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-80 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-82 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-84 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-85 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-86 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-87 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-88 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-89 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-90 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-91 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-92 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-93 | IndexStmt |
| database/migrations/003_service_operations.sql:statement-94 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-95 | IndexStmt |
| database/migrations/003_service_operations.sql:statement-96 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-97 | IndexStmt |
| database/migrations/003_service_operations.sql:statement-98 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-99 | IndexStmt |
| database/migrations/003_service_operations.sql:statement-100 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-101 | IndexStmt |
| database/migrations/003_service_operations.sql:statement-102 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-103 | IndexStmt |
| database/migrations/003_service_operations.sql:statement-104 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-105 | IndexStmt |
| database/migrations/003_service_operations.sql:statement-106 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-107 | IndexStmt |
| database/migrations/003_service_operations.sql:statement-108 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-109 | IndexStmt |
| database/migrations/003_service_operations.sql:statement-110 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-111 | IndexStmt |
| database/migrations/003_service_operations.sql:statement-112 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-113 | IndexStmt |
| database/migrations/003_service_operations.sql:statement-114 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-115 | IndexStmt |
| database/migrations/003_service_operations.sql:statement-116 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-117 | IndexStmt |
| database/migrations/003_service_operations.sql:statement-118 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-119 | IndexStmt |
| database/migrations/003_service_operations.sql:statement-120 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-121 | IndexStmt |
| database/migrations/003_service_operations.sql:statement-122 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-123 | IndexStmt |
| database/migrations/003_service_operations.sql:statement-124 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-125 | IndexStmt |
| database/migrations/003_service_operations.sql:statement-126 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-127 | IndexStmt |
| database/migrations/003_service_operations.sql:statement-128 | CreateTrigStmt |
| database/migrations/003_service_operations.sql:statement-129 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-130 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-131 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-132 | CreateTrigStmt |
| database/migrations/003_service_operations.sql:statement-133 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-134 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-135 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-136 | CreateTrigStmt |
| database/migrations/003_service_operations.sql:statement-137 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-138 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-139 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-140 | CreateTrigStmt |
| database/migrations/003_service_operations.sql:statement-141 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-142 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-143 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-144 | CreateTrigStmt |
| database/migrations/003_service_operations.sql:statement-145 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-146 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-147 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-148 | CreateTrigStmt |
| database/migrations/003_service_operations.sql:statement-149 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-150 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-151 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-152 | CreateStmt |
| database/migrations/003_service_operations.sql:statement-164 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-165 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-166 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-167 | IndexStmt |
| database/migrations/003_service_operations.sql:statement-168 | IndexStmt |
| database/migrations/003_service_operations.sql:statement-169 | IndexStmt |
| database/migrations/003_service_operations.sql:statement-170 | CreateTrigStmt |
| database/migrations/003_service_operations.sql:statement-171 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-172 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-173 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-174 | CreateFunctionStmt |
| database/migrations/003_service_operations.sql:statement-175 | CreateFunctionStmt |
| database/migrations/003_service_operations.sql:statement-176 | CreateFunctionStmt |
| database/migrations/003_service_operations.sql:statement-177 | CreateTrigStmt |
| database/migrations/003_service_operations.sql:statement-178 | CreateTrigStmt |
| database/migrations/003_service_operations.sql:statement-179 | CreateTrigStmt |
| database/migrations/003_service_operations.sql:statement-180 | CreateTrigStmt |
| database/migrations/003_service_operations.sql:statement-181 | CreateTrigStmt |
| database/migrations/003_service_operations.sql:statement-183 | GrantStmt |
| database/migrations/003_service_operations.sql:statement-184 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-186 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-187 | IndexStmt |
| database/migrations/003_service_operations.sql:statement-188 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-189 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-190 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-191 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-192 | CreateFunctionStmt |
| database/migrations/003_service_operations.sql:statement-193 | CreateFunctionStmt |
| database/migrations/003_service_operations.sql:statement-194 | CreateFunctionStmt |
| database/migrations/003_service_operations.sql:statement-195 | CreateTrigStmt |
| database/migrations/003_service_operations.sql:statement-196 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-197 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-198 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-199 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-200 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-201 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-202 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-203 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-204 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-205 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-206 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-207 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-208 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-209 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-210 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-211 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-212 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-213 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-214 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-215 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-216 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-217 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-218 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-219 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-220 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-221 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-222 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-223 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-224 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-225 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-226 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-227 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-228 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-229 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-230 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-231 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-232 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-233 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-234 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-235 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-236 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-237 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-238 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-239 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-240 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-241 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-242 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-243 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-244 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-246 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-247 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-249 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-251 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-252 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-253 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-255 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-257 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-258 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-259 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-261 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-263 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-264 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-266 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-267 | IndexStmt |
| database/migrations/003_service_operations.sql:statement-268 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-269 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-270 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-271 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-272 | CreatePolicyStmt |
| database/migrations/003_service_operations.sql:statement-273 | CreateFunctionStmt |
| database/migrations/003_service_operations.sql:statement-274 | CreateTrigStmt |
| database/migrations/003_service_operations.sql:statement-275 | CreateTrigStmt |
| database/migrations/003_service_operations.sql:statement-276 | CreateFunctionStmt |
| database/migrations/003_service_operations.sql:statement-277 | CreateTrigStmt |
| database/migrations/003_service_operations.sql:statement-278 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-279 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-280 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-281 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-282 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-283 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-284 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-285 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-286 | AlterTableStmt |
| database/migrations/003_service_operations.sql:statement-287 | AlterTableStmt |
| database/migrations/004_backup_restore.sql:statement-1 | CreateStmt |
| database/migrations/004_backup_restore.sql:statement-8 | AlterTableStmt |
| database/migrations/004_backup_restore.sql:statement-9 | IndexStmt |
| database/migrations/004_backup_restore.sql:statement-10 | CreateStmt |
| database/migrations/004_backup_restore.sql:statement-20 | AlterTableStmt |
| database/migrations/004_backup_restore.sql:statement-21 | AlterTableStmt |
| database/migrations/004_backup_restore.sql:statement-22 | IndexStmt |
| database/migrations/004_backup_restore.sql:statement-23 | IndexStmt |
| database/migrations/004_backup_restore.sql:statement-24 | IndexStmt |
| database/migrations/004_backup_restore.sql:statement-25 | CreateFunctionStmt |
| database/migrations/004_backup_restore.sql:statement-26 | CreateFunctionStmt |
| database/migrations/004_backup_restore.sql:statement-27 | CreateTrigStmt |
| database/migrations/004_backup_restore.sql:statement-28 | CreateTrigStmt |
| database/migrations/004_backup_restore.sql:statement-29 | AlterTableStmt |
| database/migrations/004_backup_restore.sql:statement-30 | AlterTableStmt |
| database/migrations/004_backup_restore.sql:statement-31 | CreatePolicyStmt |
| database/migrations/004_backup_restore.sql:statement-32 | AlterTableStmt |
| database/migrations/004_backup_restore.sql:statement-33 | AlterTableStmt |
| database/migrations/004_backup_restore.sql:statement-34 | CreatePolicyStmt |
| database/migrations/005_manual_duration.sql:statement-1 | AlterTableStmt |
| database/migrations/005_manual_duration.sql:statement-3 | AlterTableStmt |
| database/migrations/005_manual_duration.sql:statement-5 | AlterTableStmt |
| database/migrations/005_manual_duration.sql:statement-6 | AlterTableStmt |
| database/migrations/005_manual_duration.sql:statement-7 | AlterTableStmt |
| database/migrations/005_manual_duration.sql:statement-8 | CreateFunctionStmt |
| database/migrations/005_manual_duration.sql:statement-9 | CreateTrigStmt |
| database/migrations/005_manual_duration.sql:statement-10 | DoStmt |

## database/migrations/002_relational_schema.sql:statement-1

```sql
CREATE EXTENSION IF NOT EXISTS vector
```

## database/migrations/002_relational_schema.sql:statement-2

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist
```

## database/migrations/002_relational_schema.sql:statement-699

```sql
ALTER TABLE recipeweave.food ADD CONSTRAINT fk_food_parent_id
FOREIGN KEY (parent_id) REFERENCES recipeweave.food (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-701

```sql
ALTER TABLE recipeweave.food ADD CONSTRAINT fk_food_release_id
FOREIGN KEY (release_id) REFERENCES recipeweave.catalog_release (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-703

```sql
ALTER TABLE recipeweave.food_alias ADD CONSTRAINT fk_food_alias_food_id
FOREIGN KEY (food_id) REFERENCES recipeweave.food (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-705

```sql
ALTER TABLE recipeweave.food_form ADD CONSTRAINT fk_food_form_food_id
FOREIGN KEY (food_id) REFERENCES recipeweave.food (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-707

```sql
ALTER TABLE recipeweave.food_form ADD CONSTRAINT fk_food_form_base_unit_id
FOREIGN KEY (base_unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-709

```sql
ALTER TABLE recipeweave.conversion ADD CONSTRAINT fk_conversion_form_id
FOREIGN KEY (form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-711

```sql
ALTER TABLE recipeweave.conversion ADD CONSTRAINT fk_conversion_from_unit_id
FOREIGN KEY (from_unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-713

```sql
ALTER TABLE recipeweave.conversion ADD CONSTRAINT fk_conversion_to_unit_id
FOREIGN KEY (to_unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-715

```sql
ALTER TABLE recipeweave.conversion ADD CONSTRAINT fk_conversion_source_id
FOREIGN KEY (source_id) REFERENCES recipeweave.source_record (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-717

```sql
ALTER TABLE recipeweave.conversion ADD CONSTRAINT fk_conversion_release_id
FOREIGN KEY (release_id) REFERENCES recipeweave.catalog_release (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-719

```sql
ALTER TABLE recipeweave.form_yield ADD CONSTRAINT fk_form_yield_input_form_id
FOREIGN KEY (input_form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-721

```sql
ALTER TABLE recipeweave.form_yield ADD CONSTRAINT fk_form_yield_output_form_id
FOREIGN KEY (output_form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-723

```sql
ALTER TABLE recipeweave.form_yield ADD CONSTRAINT fk_form_yield_source_id
FOREIGN KEY (source_id) REFERENCES recipeweave.source_record (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-725

```sql
ALTER TABLE recipeweave.product ADD CONSTRAINT fk_product_food_id
FOREIGN KEY (food_id) REFERENCES recipeweave.food (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-727

```sql
ALTER TABLE recipeweave.product_version ADD CONSTRAINT fk_product_version_product_id
FOREIGN KEY (product_id) REFERENCES recipeweave.product (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-729

```sql
ALTER TABLE recipeweave.product_version ADD CONSTRAINT fk_product_version_form_id
FOREIGN KEY (form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-731

```sql
ALTER TABLE recipeweave.product_version ADD CONSTRAINT fk_product_version_unit_id
FOREIGN KEY (unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-733

```sql
ALTER TABLE recipeweave.product_version ADD CONSTRAINT fk_product_version_source_id
FOREIGN KEY (source_id) REFERENCES recipeweave.source_record (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-735

```sql
ALTER TABLE recipeweave.product_component ADD CONSTRAINT fk_product_component_product_version_id
FOREIGN KEY (product_version_id) REFERENCES recipeweave.product_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-737

```sql
ALTER TABLE recipeweave.product_component ADD CONSTRAINT fk_product_component_form_id
FOREIGN KEY (form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-739

```sql
ALTER TABLE recipeweave.product_component ADD CONSTRAINT fk_product_component_unit_id
FOREIGN KEY (unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-741

```sql
ALTER TABLE recipeweave.allergen ADD CONSTRAINT fk_allergen_source_id
FOREIGN KEY (source_id) REFERENCES recipeweave.source_record (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-743

```sql
ALTER TABLE recipeweave.food_allergen ADD CONSTRAINT fk_food_allergen_form_id
FOREIGN KEY (form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-745

```sql
ALTER TABLE recipeweave.food_allergen ADD CONSTRAINT fk_food_allergen_allergen_id
FOREIGN KEY (allergen_id) REFERENCES recipeweave.allergen (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-747

```sql
ALTER TABLE recipeweave.food_allergen ADD CONSTRAINT fk_food_allergen_source_id
FOREIGN KEY (source_id) REFERENCES recipeweave.source_record (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-749

```sql
ALTER TABLE recipeweave.product_allergen ADD CONSTRAINT fk_product_allergen_product_version_id
FOREIGN KEY (product_version_id) REFERENCES recipeweave.product_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-751

```sql
ALTER TABLE recipeweave.product_allergen ADD CONSTRAINT fk_product_allergen_allergen_id
FOREIGN KEY (allergen_id) REFERENCES recipeweave.allergen (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-753

```sql
ALTER TABLE recipeweave.product_allergen ADD CONSTRAINT fk_product_allergen_source_id
FOREIGN KEY (source_id) REFERENCES recipeweave.source_record (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-755

```sql
ALTER TABLE recipeweave.nutrition_fact ADD CONSTRAINT fk_nutrition_fact_form_id
FOREIGN KEY (form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-757

```sql
ALTER TABLE recipeweave.nutrition_fact ADD CONSTRAINT fk_nutrition_fact_product_version_id
FOREIGN KEY (product_version_id) REFERENCES recipeweave.product_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-759

```sql
ALTER TABLE recipeweave.nutrition_fact ADD CONSTRAINT fk_nutrition_fact_nutrient_id
FOREIGN KEY (nutrient_id) REFERENCES recipeweave.nutrient (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-761

```sql
ALTER TABLE recipeweave.nutrition_fact ADD CONSTRAINT fk_nutrition_fact_basis_unit_id
FOREIGN KEY (basis_unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-763

```sql
ALTER TABLE recipeweave.nutrition_fact ADD CONSTRAINT fk_nutrition_fact_source_id
FOREIGN KEY (source_id) REFERENCES recipeweave.source_record (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-765

```sql
ALTER TABLE recipeweave.axis ADD CONSTRAINT fk_axis_release_id
FOREIGN KEY (release_id) REFERENCES recipeweave.catalog_release (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-767

```sql
ALTER TABLE recipeweave.axis_option ADD CONSTRAINT fk_axis_option_axis_id
FOREIGN KEY (axis_id) REFERENCES recipeweave.axis (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-769

```sql
ALTER TABLE recipeweave.axis_option ADD CONSTRAINT fk_axis_option_parent_id
FOREIGN KEY (parent_id) REFERENCES recipeweave.axis_option (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-771

```sql
ALTER TABLE recipeweave.food_axis_option ADD CONSTRAINT fk_food_axis_option_food_id
FOREIGN KEY (food_id) REFERENCES recipeweave.food (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-773

```sql
ALTER TABLE recipeweave.food_axis_option ADD CONSTRAINT fk_food_axis_option_option_id
FOREIGN KEY (option_id) REFERENCES recipeweave.axis_option (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-775

```sql
ALTER TABLE recipeweave.recipe ADD CONSTRAINT fk_recipe_family_option_id
FOREIGN KEY (family_option_id) REFERENCES recipeweave.axis_option (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-777

```sql
ALTER TABLE recipeweave.recipe_version ADD CONSTRAINT fk_recipe_version_recipe_id
FOREIGN KEY (recipe_id) REFERENCES recipeweave.recipe (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-779

```sql
ALTER TABLE recipeweave.recipe_version ADD CONSTRAINT fk_recipe_version_release_id
FOREIGN KEY (release_id) REFERENCES recipeweave.catalog_release (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-781

```sql
ALTER TABLE recipeweave.recipe_version ADD CONSTRAINT fk_recipe_version_output_unit_id
FOREIGN KEY (output_unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-783

```sql
ALTER TABLE recipeweave.recipe_option ADD CONSTRAINT fk_recipe_option_recipe_version_id
FOREIGN KEY (recipe_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-785

```sql
ALTER TABLE recipeweave.recipe_option ADD CONSTRAINT fk_recipe_option_option_id
FOREIGN KEY (option_id) REFERENCES recipeweave.axis_option (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-787

```sql
ALTER TABLE recipeweave.scaling_rule ADD CONSTRAINT fk_scaling_rule_source_id
FOREIGN KEY (source_id) REFERENCES recipeweave.source_record (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-789

```sql
ALTER TABLE recipeweave.scaling_point ADD CONSTRAINT fk_scaling_point_rule_id
FOREIGN KEY (rule_id) REFERENCES recipeweave.scaling_rule (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-791

```sql
ALTER TABLE recipeweave.recipe_ingredient ADD CONSTRAINT fk_recipe_ingredient_recipe_version_id
FOREIGN KEY (recipe_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-793

```sql
ALTER TABLE recipeweave.recipe_ingredient ADD CONSTRAINT fk_recipe_ingredient_form_id
FOREIGN KEY (form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-795

```sql
ALTER TABLE recipeweave.recipe_ingredient ADD CONSTRAINT fk_recipe_ingredient_product_version_id
FOREIGN KEY (product_version_id) REFERENCES recipeweave.product_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-797

```sql
ALTER TABLE recipeweave.recipe_ingredient ADD CONSTRAINT fk_recipe_ingredient_component_id
FOREIGN KEY (component_id) REFERENCES recipeweave.product_component (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-799

```sql
ALTER TABLE recipeweave.recipe_ingredient ADD CONSTRAINT fk_recipe_ingredient_kit_parent_line_id
FOREIGN KEY (kit_parent_line_id) REFERENCES recipeweave.recipe_ingredient (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-801

```sql
ALTER TABLE recipeweave.recipe_ingredient ADD CONSTRAINT fk_recipe_ingredient_unit_id
FOREIGN KEY (unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-803

```sql
ALTER TABLE recipeweave.recipe_ingredient ADD CONSTRAINT fk_recipe_ingredient_conversion_id
FOREIGN KEY (conversion_id) REFERENCES recipeweave.conversion (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-805

```sql
ALTER TABLE recipeweave.recipe_ingredient ADD CONSTRAINT fk_recipe_ingredient_scaling_rule_id
FOREIGN KEY (scaling_rule_id) REFERENCES recipeweave.scaling_rule (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-807

```sql
ALTER TABLE recipeweave.operation_parameter ADD CONSTRAINT fk_operation_parameter_operation_id
FOREIGN KEY (operation_id) REFERENCES recipeweave.operation (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-809

```sql
ALTER TABLE recipeweave.operation_parameter ADD CONSTRAINT fk_operation_parameter_unit_id
FOREIGN KEY (unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-811

```sql
ALTER TABLE recipeweave.recipe_step ADD CONSTRAINT fk_recipe_step_recipe_version_id
FOREIGN KEY (recipe_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-813

```sql
ALTER TABLE recipeweave.recipe_step ADD CONSTRAINT fk_recipe_step_operation_id
FOREIGN KEY (operation_id) REFERENCES recipeweave.operation (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-815

```sql
ALTER TABLE recipeweave.recipe_step ADD CONSTRAINT fk_recipe_step_scaling_rule_id
FOREIGN KEY (scaling_rule_id) REFERENCES recipeweave.scaling_rule (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-817

```sql
ALTER TABLE recipeweave.step_parameter ADD CONSTRAINT fk_step_parameter_step_id
FOREIGN KEY (step_id) REFERENCES recipeweave.recipe_step (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-819

```sql
ALTER TABLE recipeweave.step_parameter ADD CONSTRAINT fk_step_parameter_parameter_id
FOREIGN KEY (parameter_id) REFERENCES recipeweave.operation_parameter (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-821

```sql
ALTER TABLE recipeweave.material_node ADD CONSTRAINT fk_material_node_recipe_version_id
FOREIGN KEY (recipe_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-823

```sql
ALTER TABLE recipeweave.material_node ADD CONSTRAINT fk_material_node_ingredient_line_id
FOREIGN KEY (ingredient_line_id) REFERENCES recipeweave.recipe_ingredient (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-825

```sql
ALTER TABLE recipeweave.material_node ADD CONSTRAINT fk_material_node_producer_step_id
FOREIGN KEY (producer_step_id) REFERENCES recipeweave.recipe_step (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-827

```sql
ALTER TABLE recipeweave.material_node ADD CONSTRAINT fk_material_node_unit_id
FOREIGN KEY (unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-829

```sql
ALTER TABLE recipeweave.step_input ADD CONSTRAINT fk_step_input_step_id
FOREIGN KEY (step_id) REFERENCES recipeweave.recipe_step (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-831

```sql
ALTER TABLE recipeweave.step_input ADD CONSTRAINT fk_step_input_material_id
FOREIGN KEY (material_id) REFERENCES recipeweave.material_node (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-833

```sql
ALTER TABLE recipeweave.step_dependency ADD CONSTRAINT fk_step_dependency_before_step_id
FOREIGN KEY (before_step_id) REFERENCES recipeweave.recipe_step (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-835

```sql
ALTER TABLE recipeweave.step_dependency ADD CONSTRAINT fk_step_dependency_after_step_id
FOREIGN KEY (after_step_id) REFERENCES recipeweave.recipe_step (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-837

```sql
ALTER TABLE recipeweave.resource_type ADD CONSTRAINT fk_resource_type_capacity_unit_id
FOREIGN KEY (capacity_unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-839

```sql
ALTER TABLE recipeweave.step_resource ADD CONSTRAINT fk_step_resource_step_id
FOREIGN KEY (step_id) REFERENCES recipeweave.recipe_step (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-841

```sql
ALTER TABLE recipeweave.step_resource ADD CONSTRAINT fk_step_resource_resource_type_id
FOREIGN KEY (resource_type_id) REFERENCES recipeweave.resource_type (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-843

```sql
ALTER TABLE recipeweave.media_asset ADD CONSTRAINT fk_media_asset_operation_id
FOREIGN KEY (operation_id) REFERENCES recipeweave.operation (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-845

```sql
ALTER TABLE recipeweave.media_asset ADD CONSTRAINT fk_media_asset_source_id
FOREIGN KEY (source_id) REFERENCES recipeweave.source_record (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-847

```sql
ALTER TABLE recipeweave.step_media ADD CONSTRAINT fk_step_media_step_id
FOREIGN KEY (step_id) REFERENCES recipeweave.recipe_step (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-849

```sql
ALTER TABLE recipeweave.step_media ADD CONSTRAINT fk_step_media_media_id
FOREIGN KEY (media_id) REFERENCES recipeweave.media_asset (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-851

```sql
ALTER TABLE recipeweave.generation_policy ADD CONSTRAINT fk_generation_policy_release_id
FOREIGN KEY (release_id) REFERENCES recipeweave.catalog_release (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-853

```sql
ALTER TABLE recipeweave.generation_job ADD CONSTRAINT fk_generation_job_policy_id
FOREIGN KEY (policy_id) REFERENCES recipeweave.generation_policy (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-855

```sql
ALTER TABLE recipeweave.generation_choice ADD CONSTRAINT fk_generation_choice_job_id
FOREIGN KEY (job_id) REFERENCES recipeweave.generation_job (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-857

```sql
ALTER TABLE recipeweave.generation_choice ADD CONSTRAINT fk_generation_choice_option_id
FOREIGN KEY (option_id) REFERENCES recipeweave.axis_option (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-859

```sql
ALTER TABLE recipeweave.generation_food ADD CONSTRAINT fk_generation_food_job_id
FOREIGN KEY (job_id) REFERENCES recipeweave.generation_job (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-861

```sql
ALTER TABLE recipeweave.generation_food ADD CONSTRAINT fk_generation_food_form_id
FOREIGN KEY (form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-863

```sql
ALTER TABLE recipeweave.generation_result ADD CONSTRAINT fk_generation_result_recipe_version_id
FOREIGN KEY (recipe_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-865

```sql
ALTER TABLE recipeweave.generation_result ADD CONSTRAINT fk_generation_result_job_id
FOREIGN KEY (job_id) REFERENCES recipeweave.generation_job (id)
ON DELETE SET NULL ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-867

```sql
ALTER TABLE recipeweave.generation_result ADD CONSTRAINT fk_generation_result_policy_id
FOREIGN KEY (policy_id) REFERENCES recipeweave.generation_policy (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-869

```sql
ALTER TABLE recipeweave.compatibility_rule ADD CONSTRAINT fk_compatibility_rule_source_id
FOREIGN KEY (source_id) REFERENCES recipeweave.source_record (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-871

```sql
ALTER TABLE recipeweave.validation_result ADD CONSTRAINT fk_validation_result_recipe_version_id
FOREIGN KEY (recipe_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-873

```sql
ALTER TABLE recipeweave.validation_result ADD CONSTRAINT fk_validation_result_rule_id
FOREIGN KEY (rule_id) REFERENCES recipeweave.compatibility_rule (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-875

```sql
ALTER TABLE recipeweave.recipe_signature ADD CONSTRAINT fk_recipe_signature_recipe_version_id
FOREIGN KEY (recipe_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-877

```sql
ALTER TABLE recipeweave.recipe_similarity ADD CONSTRAINT fk_recipe_similarity_left_version_id
FOREIGN KEY (left_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-879

```sql
ALTER TABLE recipeweave.recipe_similarity ADD CONSTRAINT fk_recipe_similarity_right_version_id
FOREIGN KEY (right_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-881

```sql
ALTER TABLE recipeweave.user_preference ADD CONSTRAINT fk_user_preference_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-883

```sql
ALTER TABLE recipeweave.user_preference ADD CONSTRAINT fk_user_preference_option_id
FOREIGN KEY (option_id) REFERENCES recipeweave.axis_option (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-885

```sql
ALTER TABLE recipeweave.user_exclusion ADD CONSTRAINT fk_user_exclusion_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-887

```sql
ALTER TABLE recipeweave.user_exclusion ADD CONSTRAINT fk_user_exclusion_food_id
FOREIGN KEY (food_id) REFERENCES recipeweave.food (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-889

```sql
ALTER TABLE recipeweave.user_exclusion ADD CONSTRAINT fk_user_exclusion_allergen_id
FOREIGN KEY (allergen_id) REFERENCES recipeweave.allergen (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-891

```sql
ALTER TABLE recipeweave.user_recipe_event ADD CONSTRAINT fk_user_recipe_event_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-893

```sql
ALTER TABLE recipeweave.user_recipe_event ADD CONSTRAINT fk_user_recipe_event_recipe_version_id
FOREIGN KEY (recipe_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-895

```sql
ALTER TABLE recipeweave.menu ADD CONSTRAINT fk_menu_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-897

```sql
ALTER TABLE recipeweave.menu_item ADD CONSTRAINT fk_menu_item_menu_id
FOREIGN KEY (menu_id) REFERENCES recipeweave.menu (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-899

```sql
ALTER TABLE recipeweave.menu_item ADD CONSTRAINT fk_menu_item_recipe_version_id
FOREIGN KEY (recipe_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-901

```sql
ALTER TABLE recipeweave.menu_item ADD CONSTRAINT fk_menu_item_role_option_id
FOREIGN KEY (role_option_id) REFERENCES recipeweave.axis_option (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-903

```sql
ALTER TABLE recipeweave.menu_ingredient_override
ADD CONSTRAINT fk_menu_ingredient_override_menu_item_id
FOREIGN KEY (menu_item_id) REFERENCES recipeweave.menu_item (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-905

```sql
ALTER TABLE recipeweave.menu_ingredient_override
ADD CONSTRAINT fk_menu_ingredient_override_ingredient_line_id
FOREIGN KEY (ingredient_line_id) REFERENCES recipeweave.recipe_ingredient (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-907

```sql
ALTER TABLE recipeweave.menu_ingredient_override ADD CONSTRAINT fk_menu_ingredient_override_form_id
FOREIGN KEY (form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-909

```sql
ALTER TABLE recipeweave.menu_ingredient_override
ADD CONSTRAINT fk_menu_ingredient_override_product_version_id
FOREIGN KEY (product_version_id) REFERENCES recipeweave.product_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-911

```sql
ALTER TABLE recipeweave.kitchen_resource ADD CONSTRAINT fk_kitchen_resource_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-913

```sql
ALTER TABLE recipeweave.kitchen_resource ADD CONSTRAINT fk_kitchen_resource_resource_type_id
FOREIGN KEY (resource_type_id) REFERENCES recipeweave.resource_type (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-915

```sql
ALTER TABLE recipeweave.cooking_session ADD CONSTRAINT fk_cooking_session_menu_id
FOREIGN KEY (menu_id) REFERENCES recipeweave.menu (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-917

```sql
ALTER TABLE recipeweave.session_task ADD CONSTRAINT fk_session_task_session_id
FOREIGN KEY (session_id) REFERENCES recipeweave.cooking_session (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-919

```sql
ALTER TABLE recipeweave.session_task ADD CONSTRAINT fk_session_task_menu_item_id
FOREIGN KEY (menu_item_id) REFERENCES recipeweave.menu_item (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-921

```sql
ALTER TABLE recipeweave.session_task ADD CONSTRAINT fk_session_task_step_id
FOREIGN KEY (step_id) REFERENCES recipeweave.recipe_step (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-923

```sql
ALTER TABLE recipeweave.task_dependency ADD CONSTRAINT fk_task_dependency_before_task_id
FOREIGN KEY (before_task_id) REFERENCES recipeweave.session_task (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-925

```sql
ALTER TABLE recipeweave.task_dependency ADD CONSTRAINT fk_task_dependency_after_task_id
FOREIGN KEY (after_task_id) REFERENCES recipeweave.session_task (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-927

```sql
ALTER TABLE recipeweave.resource_reservation ADD CONSTRAINT fk_resource_reservation_task_id
FOREIGN KEY (task_id) REFERENCES recipeweave.session_task (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-929

```sql
ALTER TABLE recipeweave.resource_reservation ADD CONSTRAINT fk_resource_reservation_resource_id
FOREIGN KEY (resource_id) REFERENCES recipeweave.kitchen_resource (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-931

```sql
ALTER TABLE recipeweave.ingredient_total ADD CONSTRAINT fk_ingredient_total_session_id
FOREIGN KEY (session_id) REFERENCES recipeweave.cooking_session (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-933

```sql
ALTER TABLE recipeweave.ingredient_total ADD CONSTRAINT fk_ingredient_total_form_id
FOREIGN KEY (form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-935

```sql
ALTER TABLE recipeweave.ingredient_total ADD CONSTRAINT fk_ingredient_total_product_version_id
FOREIGN KEY (product_version_id) REFERENCES recipeweave.product_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-937

```sql
ALTER TABLE recipeweave.ingredient_total ADD CONSTRAINT fk_ingredient_total_unit_id
FOREIGN KEY (unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-939

```sql
ALTER TABLE recipeweave.pantry_lot ADD CONSTRAINT fk_pantry_lot_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-941

```sql
ALTER TABLE recipeweave.pantry_lot ADD CONSTRAINT fk_pantry_lot_form_id
FOREIGN KEY (form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-943

```sql
ALTER TABLE recipeweave.pantry_lot ADD CONSTRAINT fk_pantry_lot_product_version_id
FOREIGN KEY (product_version_id) REFERENCES recipeweave.product_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-945

```sql
ALTER TABLE recipeweave.pantry_lot ADD CONSTRAINT fk_pantry_lot_unit_id
FOREIGN KEY (unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-947

```sql
ALTER TABLE recipeweave.shopping_item ADD CONSTRAINT fk_shopping_item_session_id
FOREIGN KEY (session_id) REFERENCES recipeweave.cooking_session (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-949

```sql
ALTER TABLE recipeweave.shopping_item ADD CONSTRAINT fk_shopping_item_total_id
FOREIGN KEY (total_id) REFERENCES recipeweave.ingredient_total (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-951

```sql
ALTER TABLE recipeweave.shopping_item ADD CONSTRAINT fk_shopping_item_product_version_id
FOREIGN KEY (product_version_id) REFERENCES recipeweave.product_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-953

```sql
ALTER TABLE recipeweave.audit_event ADD CONSTRAINT fk_audit_event_actor_id
FOREIGN KEY (actor_id) REFERENCES recipeweave.app_user (id)
ON DELETE SET NULL ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-955

```sql
ALTER TABLE recipeweave.product_preparation_rule
ADD CONSTRAINT fk_product_preparation_rule_product_version_id
FOREIGN KEY (product_version_id) REFERENCES recipeweave.product_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-957

```sql
ALTER TABLE recipeweave.product_preparation_rule
ADD CONSTRAINT fk_product_preparation_rule_operation_id
FOREIGN KEY (operation_id) REFERENCES recipeweave.operation (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-959

```sql
ALTER TABLE recipeweave.product_preparation_rule
ADD CONSTRAINT fk_product_preparation_rule_source_id
FOREIGN KEY (source_id) REFERENCES recipeweave.source_record (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-961

```sql
ALTER TABLE recipeweave.food_identity_member ADD CONSTRAINT fk_food_identity_member_food_id
FOREIGN KEY (food_id) REFERENCES recipeweave.food (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-963

```sql
ALTER TABLE recipeweave.food_identity_member ADD CONSTRAINT fk_food_identity_member_identity_id
FOREIGN KEY (identity_id) REFERENCES recipeweave.food_identity (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-965

```sql
ALTER TABLE recipeweave.generation_template ADD CONSTRAINT fk_generation_template_release_id
FOREIGN KEY (release_id) REFERENCES recipeweave.catalog_release (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-967

```sql
ALTER TABLE recipeweave.generation_shard ADD CONSTRAINT fk_generation_shard_template_id
FOREIGN KEY (template_id) REFERENCES recipeweave.generation_template (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-969

```sql
ALTER TABLE recipeweave.candidate_attempt ADD CONSTRAINT fk_candidate_attempt_template_id
FOREIGN KEY (template_id) REFERENCES recipeweave.generation_template (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-971

```sql
ALTER TABLE recipeweave.candidate_attempt ADD CONSTRAINT fk_candidate_attempt_job_id
FOREIGN KEY (job_id) REFERENCES recipeweave.generation_job (id)
ON DELETE SET NULL ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-973

```sql
ALTER TABLE recipeweave.candidate_attempt ADD CONSTRAINT fk_candidate_attempt_recipe_version_id
FOREIGN KEY (recipe_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-975

```sql
ALTER TABLE recipeweave.recipe_search_document ADD CONSTRAINT fk_recipe_search_document_recipe_id
FOREIGN KEY (recipe_id) REFERENCES recipeweave.recipe (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-977

```sql
ALTER TABLE recipeweave.recipe_search_document
ADD CONSTRAINT fk_recipe_search_document_published_version_id
FOREIGN KEY (published_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-979

```sql
ALTER TABLE recipeweave.recipe_embedding ADD CONSTRAINT fk_recipe_embedding_recipe_version_id
FOREIGN KEY (recipe_version_id) REFERENCES recipeweave.recipe_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-981

```sql
ALTER TABLE recipeweave.generation_stratum_metric
ADD CONSTRAINT fk_generation_stratum_metric_template_id
FOREIGN KEY (template_id) REFERENCES recipeweave.generation_template (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/002_relational_schema.sql:statement-1001

```sql
ALTER TABLE recipeweave.generation_shard ADD CONSTRAINT generation_shard_no_overlap
EXCLUDE USING gist (template_id WITH =, INT8RANGE(start_ordinal, end_ordinal, '[)') WITH &&)
```

## database/migrations/002_relational_schema.sql:statement-1002

```sql
CREATE FUNCTION recipeweave.reject_identity_change() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.id IS DISTINCT FROM OLD.id OR NEW.created_at IS DISTINCT FROM OLD.created_at THEN
        RAISE EXCEPTION '識別子と作成日時は変更できません' USING ERRCODE = '23514';
    END IF;
    RETURN NEW;
END;
$$
```

## database/migrations/002_relational_schema.sql:statement-1003

```sql
CREATE FUNCTION recipeweave.recipe_version_for(table_name TEXT, row_data JSONB) RETURNS UUID
LANGUAGE plpgsql STABLE AS $$
DECLARE
    target uuid;
BEGIN
    IF table_name = 'recipe_version' THEN
        RETURN (row_data->>'id')::uuid;
    ELSIF row_data ? 'recipe_version_id' THEN
        RETURN (row_data->>'recipe_version_id')::uuid;
    ELSIF table_name IN ('step_parameter', 'step_input', 'step_resource', 'step_media') THEN
        SELECT recipe_version_id INTO target FROM recipeweave.recipe_step
        WHERE id = (row_data->>'step_id')::uuid;
    ELSIF table_name = 'step_dependency' THEN
        SELECT recipe_version_id INTO target FROM recipeweave.recipe_step
        WHERE id = (row_data->>'before_step_id')::uuid;
    END IF;
    RETURN target;
END;
$$
```

## database/migrations/002_relational_schema.sql:statement-1004

```sql
CREATE FUNCTION recipeweave.guard_recipe_content() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
DECLARE
    row_data jsonb;
    version_id uuid;
    released boolean;
BEGIN
    row_data := CASE WHEN TG_OP = 'DELETE' THEN to_jsonb(OLD) ELSE to_jsonb(NEW) END;
    version_id := recipeweave.recipe_version_for(TG_TABLE_NAME, row_data);
    SELECT published_at IS NOT NULL INTO released FROM recipeweave.recipe_version WHERE id = version_id;
    IF TG_TABLE_NAME = 'recipe_version' AND TG_OP = 'UPDATE' AND to_jsonb(OLD)->>'published_at' IS NOT NULL THEN
        IF (to_jsonb(NEW) - 'status') IS DISTINCT FROM (to_jsonb(OLD) - 'status')
           OR NEW.status NOT IN ('published', 'withdrawn') THEN
            RAISE EXCEPTION '公開したレシピ版の内容は変更できません' USING ERRCODE = '23514';
        END IF;
    ELSIF released THEN
        RAISE EXCEPTION '公開したレシピ版とその子行は変更・削除できません' USING ERRCODE = '23514';
    END IF;
    IF TG_OP = 'UPDATE' AND TG_TABLE_NAME <> 'recipe_version' THEN
        version_id := recipeweave.recipe_version_for(TG_TABLE_NAME, to_jsonb(OLD));
        IF EXISTS (SELECT 1 FROM recipeweave.recipe_version WHERE id = version_id AND published_at IS NOT NULL) THEN
            RAISE EXCEPTION '公開版から子行を移動できません' USING ERRCODE = '23514';
        END IF;
    END IF;
    RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
END;
$$
```

## database/migrations/002_relational_schema.sql:statement-1005

```sql
CREATE FUNCTION recipeweave.validate_recipe_version(version_id UUID) RETURNS VOID
LANGUAGE plpgsql AS $$
DECLARE
    current_version recipeweave.recipe_version%ROWTYPE;
BEGIN
    SELECT * INTO current_version FROM recipeweave.recipe_version WHERE id = version_id FOR UPDATE;
    IF NOT FOUND THEN RETURN; END IF;
    IF EXISTS (
        SELECT 1 FROM recipeweave.recipe_ingredient i
        LEFT JOIN recipeweave.recipe_ingredient parent ON parent.id = i.kit_parent_line_id
        LEFT JOIN recipeweave.product_component component ON component.id = i.component_id
        LEFT JOIN recipeweave.product_version product ON product.id = i.product_version_id
        WHERE i.recipe_version_id = version_id AND (
            (i.product_version_id IS NOT NULL AND product.form_id <> i.form_id)
            OR (i.demand_kind = 'kit_component' AND (
                parent.recipe_version_id <> version_id OR parent.demand_kind <> 'purchase'
                OR parent.product_version_id IS NULL
                OR component.product_version_id <> parent.product_version_id
                OR component.form_id <> i.form_id
            ))
        )
    ) THEN RAISE EXCEPTION '商品・形態・セット親の所属が一致しません' USING ERRCODE = '23514'; END IF;
    IF EXISTS (
        SELECT 1 FROM recipeweave.recipe_ingredient i
        JOIN recipeweave.food_form form ON form.id = i.form_id
        JOIN recipeweave.unit input_unit ON input_unit.id = i.unit_id
        JOIN recipeweave.unit base_unit ON base_unit.id = form.base_unit_id
        LEFT JOIN recipeweave.conversion c ON c.id = i.conversion_id
        WHERE i.recipe_version_id = version_id AND (
            (i.conversion_id IS NOT NULL AND (c.form_id <> i.form_id OR c.from_unit_id <> i.unit_id
                OR c.to_unit_id <> form.base_unit_id OR c.release_id <> current_version.release_id))
            OR (i.amount_mode = 'exact' AND (
                (i.conversion_id IS NULL AND input_unit.dimension <> base_unit.dimension)
                OR i.canonical_amount <> round(CASE WHEN c.id IS NOT NULL THEN i.amount * c.factor
                    ELSE (i.amount * input_unit.factor + input_unit.offset - base_unit.offset) / base_unit.factor END, 6)
            ))
        )
    ) THEN RAISE EXCEPTION '形態専用換算と登録基準量が一致しません' USING ERRCODE = '23514'; END IF;
    IF EXISTS (
        SELECT 1 FROM recipeweave.material_node n
        LEFT JOIN recipeweave.recipe_ingredient i ON i.id = n.ingredient_line_id
        LEFT JOIN recipeweave.recipe_step s ON s.id = n.producer_step_id
        WHERE n.recipe_version_id = version_id
          AND (i.recipe_version_id <> version_id OR s.recipe_version_id <> version_id)
    ) OR EXISTS (
        SELECT 1 FROM recipeweave.step_input input
        JOIN recipeweave.recipe_step s ON s.id = input.step_id
        JOIN recipeweave.material_node n ON n.id = input.material_id
        WHERE (s.recipe_version_id = version_id OR n.recipe_version_id = version_id)
          AND s.recipe_version_id <> n.recipe_version_id
    ) OR EXISTS (
        SELECT 1 FROM recipeweave.step_dependency d
        JOIN recipeweave.recipe_step b ON b.id = d.before_step_id
        JOIN recipeweave.recipe_step a ON a.id = d.after_step_id
        WHERE (b.recipe_version_id = version_id OR a.recipe_version_id = version_id)
          AND b.recipe_version_id <> a.recipe_version_id
    ) THEN RAISE EXCEPTION '材料と工程を別のレシピ版へ接続できません' USING ERRCODE = '23514'; END IF;
    IF EXISTS (
        SELECT 1 FROM recipeweave.step_input i JOIN recipeweave.material_node n ON n.id = i.material_id
        WHERE n.recipe_version_id = version_id GROUP BY n.id HAVING sum(i.fraction) > 1
    ) THEN RAISE EXCEPTION '材料の使用割合が全量を超えています' USING ERRCODE = '23514'; END IF;
    IF EXISTS (
        WITH RECURSIVE edges AS (
            SELECT d.before_step_id AS before_id, d.after_step_id AS after_id
            FROM recipeweave.step_dependency d JOIN recipeweave.recipe_step s ON s.id = d.before_step_id
            WHERE s.recipe_version_id = version_id
            UNION
            SELECT n.producer_step_id, i.step_id FROM recipeweave.material_node n
            JOIN recipeweave.step_input i ON i.material_id = n.id
            WHERE n.recipe_version_id = version_id AND n.producer_step_id IS NOT NULL
        ), reach(before_id, after_id) AS (
            SELECT before_id, after_id FROM edges
            UNION
            SELECT r.before_id, e.after_id FROM reach r JOIN edges e ON e.before_id = r.after_id
        ) SELECT 1 FROM reach WHERE before_id = after_id
    ) THEN RAISE EXCEPTION '工程・材料の依存に循環があります' USING ERRCODE = '23514'; END IF;
    IF EXISTS (
        SELECT 1 FROM recipeweave.step_parameter value
        JOIN recipeweave.recipe_step step ON step.id = value.step_id
        JOIN recipeweave.operation_parameter parameter ON parameter.id = value.parameter_id
        WHERE step.recipe_version_id = version_id AND (
            step.operation_id <> parameter.operation_id
            OR (parameter.value_type IN ('decimal', 'integer') AND (value.number_value IS NULL
                OR value.number_value < parameter.min_value OR value.number_value > parameter.max_value))
            OR (parameter.value_type = 'integer' AND value.number_value <> trunc(value.number_value))
            OR (parameter.value_type = 'boolean' AND value.bool_value IS NULL)
            OR (parameter.value_type IN ('text', 'option') AND value.text_value IS NULL)
            OR (parameter.value_type = 'option' AND NOT parameter.allowed_values ? value.text_value)
        )
    ) THEN RAISE EXCEPTION '工程パラメータの動作・型・範囲が不一致です' USING ERRCODE = '23514'; END IF;
    IF EXISTS (
        SELECT 1 FROM recipeweave.step_media mapping
        JOIN recipeweave.recipe_step step ON step.id = mapping.step_id
        JOIN recipeweave.media_asset media ON media.id = mapping.media_id
        WHERE step.recipe_version_id = version_id AND step.operation_id <> media.operation_id
    ) THEN RAISE EXCEPTION '工程と媒体の標準動作が一致しません' USING ERRCODE = '23514'; END IF;
    IF EXISTS (
        SELECT 1 FROM recipeweave.recipe_option ro
        JOIN recipeweave.axis_option ao ON ao.id = ro.option_id JOIN recipeweave.axis axis ON axis.id = ao.axis_id
        WHERE ro.recipe_version_id = version_id AND axis.release_id <> current_version.release_id
    ) OR EXISTS (
        SELECT 1 FROM recipeweave.recipe_ingredient i JOIN recipeweave.food_form form ON form.id = i.form_id
        JOIN recipeweave.food food ON food.id = form.food_id
        WHERE i.recipe_version_id = version_id AND food.release_id <> current_version.release_id
    ) THEN RAISE EXCEPTION '食材・分類と採用カタログ版が一致しません' USING ERRCODE = '23514'; END IF;
    IF EXISTS (
        SELECT 1 FROM recipeweave.recipe_option ro JOIN recipeweave.axis_option ao ON ao.id = ro.option_id
        JOIN recipeweave.axis axis ON axis.id = ao.axis_id
        WHERE ro.recipe_version_id = version_id AND axis.selection = 'single'
        GROUP BY axis.id HAVING count(*) > 1
    ) THEN RAISE EXCEPTION '単一選択軸に複数値を設定できません' USING ERRCODE = '23514'; END IF;
    IF current_version.status = 'published' THEN
        IF NOT EXISTS (SELECT 1 FROM recipeweave.catalog_release
            WHERE id = current_version.release_id AND published_at IS NOT NULL) THEN
            RAISE EXCEPTION '公開版は公開済みカタログを参照する必要があります' USING ERRCODE = '23514';
        END IF;
        IF EXISTS (SELECT 1 FROM recipeweave.recipe_ingredient ingredient
            JOIN recipeweave.food_form form ON form.id = ingredient.form_id
            JOIN recipeweave.food food ON food.id = form.food_id
            WHERE ingredient.recipe_version_id = version_id AND food.owner_id IS NOT NULL) THEN
            RAISE EXCEPTION '私有食材を含むレシピは公開できません' USING ERRCODE = '23514';
        END IF;
        IF NOT EXISTS (SELECT 1 FROM recipeweave.recipe_ingredient WHERE recipe_version_id = version_id)
           OR NOT EXISTS (SELECT 1 FROM recipeweave.recipe_step WHERE recipe_version_id = version_id) THEN
            RAISE EXCEPTION '材料または工程のないレシピは公開できません' USING ERRCODE = '23514';
        END IF;
        IF EXISTS (
            SELECT 1 FROM recipeweave.recipe_step s JOIN recipeweave.operation_parameter p ON p.operation_id = s.operation_id
            WHERE s.recipe_version_id = version_id AND p.required
            AND NOT EXISTS (SELECT 1 FROM recipeweave.step_parameter v WHERE v.step_id = s.id AND v.parameter_id = p.id)
        ) THEN RAISE EXCEPTION '必須の工程パラメータがありません' USING ERRCODE = '23514'; END IF;
        IF EXISTS (
            SELECT 1 FROM recipeweave.material_node n JOIN recipeweave.step_input i ON i.material_id = n.id
            WHERE n.recipe_version_id = version_id AND n.producer_step_id IS NOT NULL
              AND NOT EXISTS (SELECT 1 FROM recipeweave.step_dependency d WHERE d.before_step_id = n.producer_step_id
                  AND d.after_step_id = i.step_id AND d.kind = 'material')
        ) THEN RAISE EXCEPTION '生成材料の受渡しに材料依存辺がありません' USING ERRCODE = '23514'; END IF;
    END IF;
END;
$$
```

## database/migrations/002_relational_schema.sql:statement-1006

```sql
CREATE FUNCTION recipeweave.check_recipe_integrity() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
DECLARE
    version_id uuid;
BEGIN
    IF TG_OP <> 'DELETE' THEN
        version_id := recipeweave.recipe_version_for(TG_TABLE_NAME, to_jsonb(NEW));
        PERFORM recipeweave.validate_recipe_version(version_id);
    END IF;
    IF TG_OP <> 'INSERT' THEN
        version_id := recipeweave.recipe_version_for(TG_TABLE_NAME, to_jsonb(OLD));
        PERFORM recipeweave.validate_recipe_version(version_id);
    END IF;
    RETURN NULL;
END;
$$
```

## database/migrations/002_relational_schema.sql:statement-1007

```sql
CREATE FUNCTION recipeweave.check_hierarchy() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
DECLARE
    cycle_found boolean;
    parent_release uuid;
BEGIN

    EXECUTE format('SELECT * FROM recipeweave.%I WHERE id = $1', TG_TABLE_NAME) INTO NEW USING NEW.id;
    IF NEW.id IS NULL THEN RETURN NULL; END IF;
    IF TG_TABLE_NAME = 'food' THEN
        PERFORM 1 FROM recipeweave.catalog_release WHERE id = NEW.release_id FOR UPDATE;
        SELECT release_id INTO parent_release FROM recipeweave.food WHERE id = NEW.parent_id;
        IF parent_release IS DISTINCT FROM NEW.release_id AND NEW.parent_id IS NOT NULL THEN
            RAISE EXCEPTION '食材の親は同じカタログ版に属する必要があります' USING ERRCODE = '23514';
        END IF;
        WITH RECURSIVE parents(id, parent_id) AS (
            SELECT id, parent_id FROM recipeweave.food WHERE id = NEW.parent_id
            UNION
            SELECT f.id, f.parent_id FROM recipeweave.food f JOIN parents p ON f.id = p.parent_id
        ) SELECT EXISTS (SELECT 1 FROM parents WHERE id = NEW.id) INTO cycle_found;
    ELSE
        PERFORM 1 FROM recipeweave.axis WHERE id = NEW.axis_id FOR UPDATE;
        SELECT axis_id INTO parent_release FROM recipeweave.axis_option WHERE id = NEW.parent_id;
        IF parent_release IS DISTINCT FROM NEW.axis_id AND NEW.parent_id IS NOT NULL THEN
            RAISE EXCEPTION '候補値の親は同じ軸に属する必要があります' USING ERRCODE = '23514';
        END IF;
        WITH RECURSIVE parents(id, parent_id) AS (
            SELECT id, parent_id FROM recipeweave.axis_option WHERE id = NEW.parent_id
            UNION
            SELECT f.id, f.parent_id FROM recipeweave.axis_option f JOIN parents p ON f.id = p.parent_id
        ) SELECT EXISTS (SELECT 1 FROM parents WHERE id = NEW.id) INTO cycle_found;
    END IF;
    IF cycle_found THEN RAISE EXCEPTION '分類階層に循環があります' USING ERRCODE = '23514'; END IF;
    RETURN NULL;
END;
$$
```

## database/migrations/002_relational_schema.sql:statement-1008

```sql
CREATE FUNCTION recipeweave.check_cross_reference() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
DECLARE
    valid boolean := true;
BEGIN

    EXECUTE format('SELECT * FROM recipeweave.%I WHERE id = $1', TG_TABLE_NAME) INTO NEW USING NEW.id;
    IF NEW.id IS NULL THEN RETURN NULL; END IF;
    CASE TG_TABLE_NAME
    WHEN 'product_version' THEN
        SELECT p.food_id = f.food_id INTO valid FROM recipeweave.product p, recipeweave.food_form f
        WHERE p.id = NEW.product_id AND f.id = NEW.form_id;
    WHEN 'food_axis_option' THEN
        SELECT f.release_id = a.release_id INTO valid FROM recipeweave.food f,
        recipeweave.axis_option o JOIN recipeweave.axis a ON a.id = o.axis_id
        WHERE f.id = NEW.food_id AND o.id = NEW.option_id;
    WHEN 'food_identity_member' THEN
        SELECT normalizer_version = NEW.normalizer_version INTO valid
        FROM recipeweave.food_identity WHERE id = NEW.identity_id;
    WHEN 'generation_choice' THEN
        SELECT p.release_id = a.release_id INTO valid
        FROM recipeweave.generation_job j JOIN recipeweave.generation_policy p ON p.id = j.policy_id,
        recipeweave.axis_option o JOIN recipeweave.axis a ON a.id = o.axis_id
        WHERE j.id = NEW.job_id AND o.id = NEW.option_id;
    WHEN 'generation_food' THEN
        SELECT p.release_id = f.release_id INTO valid
        FROM recipeweave.generation_job j JOIN recipeweave.generation_policy p ON p.id = j.policy_id,
        recipeweave.food_form form JOIN recipeweave.food f ON f.id = form.food_id
        WHERE j.id = NEW.job_id AND form.id = NEW.form_id;
    WHEN 'generation_result' THEN
        SELECT v.release_id = p.release_id AND (NEW.job_id IS NULL OR j.policy_id = p.id) INTO valid
        FROM recipeweave.recipe_version v, recipeweave.generation_policy p
        LEFT JOIN recipeweave.generation_job j ON j.id = NEW.job_id
        WHERE v.id = NEW.recipe_version_id AND p.id = NEW.policy_id;
    WHEN 'generation_shard' THEN
        SELECT NEW.end_ordinal <= candidate_count INTO valid FROM recipeweave.generation_template WHERE id = NEW.template_id;
    WHEN 'candidate_attempt' THEN
        SELECT NEW.ordinal < candidate_count INTO valid FROM recipeweave.generation_template WHERE id = NEW.template_id;
    WHEN 'recipe_search_document' THEN
        SELECT recipe_id = NEW.recipe_id AND status = 'published' INTO valid
        FROM recipeweave.recipe_version WHERE id = NEW.published_version_id;
        valid := valid AND NOT EXISTS (SELECT 1 FROM unnest(NEW.food_identity_ids) item WHERE NOT EXISTS (
            SELECT 1 FROM recipeweave.food_identity WHERE id = item))
            AND NOT EXISTS (SELECT 1 FROM unnest(NEW.facet_option_ids) item WHERE NOT EXISTS (
                SELECT 1 FROM recipeweave.axis_option WHERE id = item));
    ELSE
        RAISE EXCEPTION '未定義の関連検査対象です';
    END CASE;
    IF NOT coalesce(valid, false) THEN RAISE EXCEPTION '参照先と版・所属・序数が一致しません' USING ERRCODE = '23514'; END IF;
    RETURN NULL;
END;
$$
```

## database/migrations/002_relational_schema.sql:statement-1009

```sql
CREATE FUNCTION recipeweave.release_for(table_name TEXT, row_data JSONB) RETURNS UUID
LANGUAGE plpgsql STABLE AS $$
DECLARE
    target uuid;
BEGIN
    IF table_name = 'catalog_release' THEN RETURN (row_data->>'id')::uuid;
    ELSIF row_data ? 'release_id' THEN RETURN (row_data->>'release_id')::uuid;
    ELSIF table_name IN ('food_alias', 'food_form', 'product', 'food_identity_member', 'food_axis_option') THEN
        SELECT release_id INTO target FROM recipeweave.food WHERE id = (row_data->>'food_id')::uuid;
    ELSIF table_name = 'axis_option' THEN
        SELECT release_id INTO target FROM recipeweave.axis WHERE id = (row_data->>'axis_id')::uuid;
    ELSIF table_name IN ('food_allergen', 'nutrition_fact') AND row_data->>'form_id' IS NOT NULL THEN
        SELECT food.release_id INTO target FROM recipeweave.food_form form
        JOIN recipeweave.food food ON food.id = form.food_id WHERE form.id = (row_data->>'form_id')::uuid;
    ELSIF table_name = 'product_version' THEN
        SELECT food.release_id INTO target FROM recipeweave.product product
        JOIN recipeweave.food food ON food.id = product.food_id WHERE product.id = (row_data->>'product_id')::uuid;
    ELSIF table_name IN ('product_component', 'product_allergen', 'product_preparation_rule', 'nutrition_fact') THEN
        SELECT food.release_id INTO target FROM recipeweave.product_version AS "version"
        JOIN recipeweave.product product ON product.id = version.product_id
        JOIN recipeweave.food food ON food.id = product.food_id WHERE version.id = (row_data->>'product_version_id')::uuid;
    END IF;
    RETURN target;
END;
$$
```

## database/migrations/002_relational_schema.sql:statement-1010

```sql
CREATE FUNCTION recipeweave.guard_catalog_content() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
DECLARE
    target uuid;
BEGIN
    IF TG_OP <> 'INSERT' THEN
        target := recipeweave.release_for(TG_TABLE_NAME, to_jsonb(OLD));
        IF EXISTS (SELECT 1 FROM recipeweave.catalog_release WHERE id = target AND published_at IS NOT NULL) THEN
            RAISE EXCEPTION '公開済みカタログの内容は変更・削除できません' USING ERRCODE = '23514';
        END IF;
    END IF;
    IF TG_OP <> 'DELETE' AND TG_TABLE_NAME <> 'catalog_release' THEN
        target := recipeweave.release_for(TG_TABLE_NAME, to_jsonb(NEW));
        PERFORM 1 FROM recipeweave.catalog_release WHERE id = target FOR UPDATE;
        IF EXISTS (SELECT 1 FROM recipeweave.catalog_release WHERE id = target AND published_at IS NOT NULL) THEN
            RAISE EXCEPTION '公開済みカタログへ内容を追加・移動できません' USING ERRCODE = '23514';
        END IF;
    END IF;
    RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
END;
$$
```

## database/migrations/002_relational_schema.sql:statement-1011

```sql
CREATE FUNCTION recipeweave.validate_cooking_session(target UUID) RETURNS VOID
LANGUAGE plpgsql AS $$
DECLARE
    session_menu uuid;
    session_owner uuid;
BEGIN
    SELECT s.menu_id, m.user_id INTO session_menu, session_owner FROM recipeweave.cooking_session s
    JOIN recipeweave.menu m ON m.id = s.menu_id WHERE s.id = target FOR UPDATE OF s;
    IF NOT FOUND THEN RETURN; END IF;
    IF EXISTS (
        SELECT 1 FROM recipeweave.session_task t
        JOIN recipeweave.menu_item item ON item.id = t.menu_item_id
        JOIN recipeweave.recipe_step step ON step.id = t.step_id
        WHERE t.session_id = target AND (item.menu_id <> session_menu OR item.recipe_version_id <> step.recipe_version_id)
    ) THEN RAISE EXCEPTION '調理タスクと献立・レシピ版が一致しません' USING ERRCODE = '23514'; END IF;
    IF EXISTS (
        SELECT 1 FROM recipeweave.task_dependency d
        JOIN recipeweave.session_task b ON b.id = d.before_task_id
        JOIN recipeweave.session_task a ON a.id = d.after_task_id
        WHERE (b.session_id = target OR a.session_id = target) AND (
            b.session_id <> a.session_id OR a.planned_start_s < b.planned_end_s + d.min_lag_s
            OR a.planned_start_s > b.planned_end_s + d.max_lag_s
        )
    ) THEN RAISE EXCEPTION 'タスクの所属または待機時間を満たせません' USING ERRCODE = '23514'; END IF;
    IF EXISTS (
        WITH RECURSIVE reach(before_id, after_id) AS (
            SELECT d.before_task_id, d.after_task_id FROM recipeweave.task_dependency d
            JOIN recipeweave.session_task t ON t.id = d.before_task_id WHERE t.session_id = target
            UNION
            SELECT r.before_id, d.after_task_id FROM reach r
            JOIN recipeweave.task_dependency d ON d.before_task_id = r.after_id
        ) SELECT 1 FROM reach WHERE before_id = after_id
    ) THEN RAISE EXCEPTION '調理タスクの依存に循環があります' USING ERRCODE = '23514'; END IF;
    IF EXISTS (
        SELECT 1 FROM recipeweave.resource_reservation r
        JOIN recipeweave.session_task t ON t.id = r.task_id
        JOIN recipeweave.kitchen_resource k ON k.id = r.resource_id
        WHERE t.session_id = target AND (k.user_id <> session_owner OR r.start_s < t.planned_start_s OR r.end_s > t.planned_end_s)
    ) THEN RAISE EXCEPTION '他人の資源またはタスク外の時間を予約できません' USING ERRCODE = '23514'; END IF;
    IF EXISTS (
        WITH reservations AS (
            SELECT r.* FROM recipeweave.resource_reservation r JOIN recipeweave.session_task t ON t.id = r.task_id
            WHERE t.session_id = target
        ) SELECT 1 FROM reservations point JOIN recipeweave.kitchen_resource k ON k.id = point.resource_id
        WHERE (SELECT sum(overlap.quantity) FROM reservations overlap WHERE overlap.resource_id = point.resource_id
            AND overlap.start_s <= point.start_s AND point.start_s < overlap.end_s) > k.quantity
    ) THEN RAISE EXCEPTION '同時予約が利用可能な資源数を超えています' USING ERRCODE = '23514'; END IF;
END;
$$
```

## database/migrations/002_relational_schema.sql:statement-1012

```sql
CREATE FUNCTION recipeweave.check_owned_reference() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
DECLARE
    target uuid;
    valid boolean := true;
BEGIN

    EXECUTE format('SELECT * FROM recipeweave.%I WHERE id = $1', TG_TABLE_NAME) INTO NEW USING NEW.id;
    IF NEW.id IS NULL THEN RETURN NULL; END IF;
    CASE TG_TABLE_NAME
    WHEN 'menu_ingredient_override' THEN
        SELECT item.recipe_version_id = ingredient.recipe_version_id INTO valid
        FROM recipeweave.menu_item item, recipeweave.recipe_ingredient ingredient
        WHERE item.id = NEW.menu_item_id AND ingredient.id = NEW.ingredient_line_id;
    WHEN 'shopping_item' THEN
        SELECT session_id = NEW.session_id INTO valid FROM recipeweave.ingredient_total WHERE id = NEW.total_id;
    WHEN 'pantry_lot' THEN
        IF NEW.product_version_id IS NOT NULL THEN
            SELECT form_id = NEW.form_id INTO valid FROM recipeweave.product_version WHERE id = NEW.product_version_id;
        END IF;
    WHEN 'session_task' THEN target := NEW.session_id;
    WHEN 'cooking_session' THEN target := NEW.id;
    WHEN 'task_dependency' THEN
        SELECT session_id INTO target FROM recipeweave.session_task WHERE id = NEW.before_task_id;
    WHEN 'resource_reservation' THEN
        PERFORM 1 FROM recipeweave.kitchen_resource WHERE id = NEW.resource_id FOR UPDATE;
        SELECT session_id INTO target FROM recipeweave.session_task WHERE id = NEW.task_id;
    ELSE RAISE EXCEPTION '未定義の所有データ検査対象です';
    END CASE;
    IF NOT coalesce(valid, false) THEN RAISE EXCEPTION '所有データの親子関係が一致しません' USING ERRCODE = '23514'; END IF;
    PERFORM recipeweave.validate_cooking_session(target);
    RETURN NULL;
END;
$$
```

## database/migrations/002_relational_schema.sql:statement-1013

```sql
CREATE FUNCTION recipeweave.guard_execution_progress() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN
    IF TG_TABLE_NAME = 'session_task' THEN
    IF OLD.status IN ('running', 'completed') AND (
        NEW.planned_start_s <> OLD.planned_start_s OR NEW.planned_end_s <> OLD.planned_end_s
        OR NEW.step_id <> OLD.step_id OR NEW.menu_item_id <> OLD.menu_item_id OR NEW.batch_no <> OLD.batch_no
        OR NEW.session_id <> OLD.session_id OR (OLD.status = 'completed' AND NEW.status <> 'completed')
    ) THEN RAISE EXCEPTION '実行中・完了済みタスクを再配置できません' USING ERRCODE = '23514'; END IF;
    END IF;
    IF TG_TABLE_NAME = 'generation_shard' THEN
    IF (
        NEW.template_id <> OLD.template_id OR NEW.start_ordinal <> OLD.start_ordinal OR NEW.end_ordinal <> OLD.end_ordinal
        OR NEW.next_ordinal < OLD.next_ordinal OR NEW.fence_token < OLD.fence_token
        OR (NEW.lease_owner IS DISTINCT FROM OLD.lease_owner AND NEW.lease_owner IS NOT NULL AND NEW.fence_token <= OLD.fence_token)
        OR (OLD.state = 'done' AND NEW.state <> 'done')
    ) THEN RAISE EXCEPTION '生成範囲・再開位置・リース世代の更新が不正です' USING ERRCODE = '23514'; END IF;
    END IF;
    RETURN NEW;
END;
$$
```

## database/migrations/002_relational_schema.sql:statement-1014

```sql
CREATE FUNCTION recipeweave.guard_audit() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN
    IF TG_OP = 'UPDATE' AND NEW.actor_id IS NULL AND OLD.actor_id IS NOT NULL
       AND (to_jsonb(NEW) - 'actor_id') = (to_jsonb(OLD) - 'actor_id') THEN RETURN NEW; END IF;
    RAISE EXCEPTION '監査イベントは追記専用です' USING ERRCODE = '23514';
END;
$$
```

## database/migrations/002_relational_schema.sql:statement-1015

```sql
CREATE FUNCTION recipeweave.publish_outbox() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
DECLARE
    identifier uuid := gen_random_uuid();
    aggregate uuid;
    event_name text;
BEGIN
    IF TG_TABLE_NAME = 'app_user' THEN
        aggregate := OLD.id;
        event_name := 'user_erased';
    ELSIF TG_TABLE_NAME = 'recipe_version' THEN
        aggregate := NEW.recipe_id;
        IF NEW.status = 'published' AND (TG_OP = 'INSERT' OR OLD.status IS DISTINCT FROM NEW.status) THEN
            event_name := 'recipe_published';
        ELSIF NEW.status = 'withdrawn' AND OLD.status IS DISTINCT FROM NEW.status THEN
            event_name := 'recipe_withdrawn';
            DELETE FROM recipeweave.recipe_search_document WHERE published_version_id = NEW.id;
            DELETE FROM recipeweave.recipe_embedding WHERE recipe_version_id = NEW.id;
        ELSE RETURN NEW;
        END IF;
    ELSE
        aggregate := NEW.id;
        IF NEW.status <> 'withdrawn' OR OLD.status = NEW.status THEN RETURN NEW; END IF;
        event_name := 'recipe_withdrawn';
        DELETE FROM recipeweave.recipe_search_document WHERE recipe_id = NEW.id;
        DELETE FROM recipeweave.recipe_embedding WHERE recipe_version_id IN (
            SELECT id FROM recipeweave.recipe_version WHERE recipe_id = NEW.id
        );
    END IF;
    INSERT INTO recipeweave.outbox_event (id, event_type, aggregate_id, payload, attempt_count)
    VALUES (identifier, event_name, aggregate, jsonb_build_object(
        'schema_version', 1, 'event_id', identifier, 'aggregate_id', aggregate, 'version', 1
    ), 0);
    RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
END;
$$
```

## database/migrations/002_relational_schema.sql:statement-1016

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.source_record
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1017

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.catalog_release
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1018

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.unit
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1019

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.food
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1020

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.food_alias
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1021

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.food_form
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1022

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.conversion
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1023

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.form_yield
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1024

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.product
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1025

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.product_version
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1026

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.product_component
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1027

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.allergen
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1028

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.food_allergen
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1029

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.product_allergen
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1030

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.nutrient
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1031

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.nutrition_fact
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1032

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.axis
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1033

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.axis_option
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1034

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.food_axis_option
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1035

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.recipe
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1036

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.recipe_version
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1037

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.recipe_option
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1038

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.scaling_rule
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1039

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.scaling_point
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1040

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.recipe_ingredient
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1041

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.operation
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1042

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.operation_parameter
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1043

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.recipe_step
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1044

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.step_parameter
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1045

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.material_node
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1046

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.step_input
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1047

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.step_dependency
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1048

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.resource_type
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1049

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.step_resource
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1050

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.media_asset
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1051

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.step_media
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1052

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.generation_policy
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1053

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.generation_job
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1054

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.generation_choice
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1055

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.generation_food
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1056

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.generation_result
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1057

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.compatibility_rule
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1058

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.validation_result
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1059

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.recipe_signature
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1060

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.recipe_similarity
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1061

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.app_user
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1062

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.user_preference
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1063

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.user_exclusion
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1064

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.user_recipe_event
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1065

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.menu
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1066

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.menu_item
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1067

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.menu_ingredient_override
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1068

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.kitchen_resource
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1069

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.cooking_session
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1070

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.session_task
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1071

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.task_dependency
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1072

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.resource_reservation
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1073

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.ingredient_total
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1074

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.pantry_lot
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1075

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.shopping_item
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1076

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.audit_event
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1077

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.outbox_event
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1078

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.product_preparation_rule
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1079

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.food_identity
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1080

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.food_identity_member
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1081

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.generation_template
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1082

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.generation_shard
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1083

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.candidate_attempt
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1084

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.recipe_search_document
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1085

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.recipe_embedding
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1086

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.generation_stratum_metric
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/002_relational_schema.sql:statement-1087

```sql
CREATE TRIGGER protect_recipe BEFORE UPDATE OR DELETE ON recipeweave.recipe_version
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_recipe_content()
```

## database/migrations/002_relational_schema.sql:statement-1088

```sql
CREATE CONSTRAINT TRIGGER recipe_integrity
AFTER INSERT OR UPDATE OR DELETE ON recipeweave.recipe_version
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_recipe_integrity()
```

## database/migrations/002_relational_schema.sql:statement-1089

```sql
CREATE TRIGGER protect_recipe BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.recipe_ingredient
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_recipe_content()
```

## database/migrations/002_relational_schema.sql:statement-1090

```sql
CREATE CONSTRAINT TRIGGER recipe_integrity
AFTER INSERT OR UPDATE OR DELETE ON recipeweave.recipe_ingredient
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_recipe_integrity()
```

## database/migrations/002_relational_schema.sql:statement-1091

```sql
CREATE TRIGGER protect_recipe BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.recipe_option
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_recipe_content()
```

## database/migrations/002_relational_schema.sql:statement-1092

```sql
CREATE CONSTRAINT TRIGGER recipe_integrity
AFTER INSERT OR UPDATE OR DELETE ON recipeweave.recipe_option
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_recipe_integrity()
```

## database/migrations/002_relational_schema.sql:statement-1093

```sql
CREATE TRIGGER protect_recipe BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.recipe_step
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_recipe_content()
```

## database/migrations/002_relational_schema.sql:statement-1094

```sql
CREATE CONSTRAINT TRIGGER recipe_integrity
AFTER INSERT OR UPDATE OR DELETE ON recipeweave.recipe_step
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_recipe_integrity()
```

## database/migrations/002_relational_schema.sql:statement-1095

```sql
CREATE TRIGGER protect_recipe BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.step_parameter
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_recipe_content()
```

## database/migrations/002_relational_schema.sql:statement-1096

```sql
CREATE CONSTRAINT TRIGGER recipe_integrity
AFTER INSERT OR UPDATE OR DELETE ON recipeweave.step_parameter
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_recipe_integrity()
```

## database/migrations/002_relational_schema.sql:statement-1097

```sql
CREATE TRIGGER protect_recipe BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.material_node
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_recipe_content()
```

## database/migrations/002_relational_schema.sql:statement-1098

```sql
CREATE CONSTRAINT TRIGGER recipe_integrity
AFTER INSERT OR UPDATE OR DELETE ON recipeweave.material_node
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_recipe_integrity()
```

## database/migrations/002_relational_schema.sql:statement-1099

```sql
CREATE TRIGGER protect_recipe BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.step_input
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_recipe_content()
```

## database/migrations/002_relational_schema.sql:statement-1100

```sql
CREATE CONSTRAINT TRIGGER recipe_integrity
AFTER INSERT OR UPDATE OR DELETE ON recipeweave.step_input
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_recipe_integrity()
```

## database/migrations/002_relational_schema.sql:statement-1101

```sql
CREATE TRIGGER protect_recipe BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.step_dependency
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_recipe_content()
```

## database/migrations/002_relational_schema.sql:statement-1102

```sql
CREATE CONSTRAINT TRIGGER recipe_integrity
AFTER INSERT OR UPDATE OR DELETE ON recipeweave.step_dependency
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_recipe_integrity()
```

## database/migrations/002_relational_schema.sql:statement-1103

```sql
CREATE TRIGGER protect_recipe BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.step_resource
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_recipe_content()
```

## database/migrations/002_relational_schema.sql:statement-1104

```sql
CREATE CONSTRAINT TRIGGER recipe_integrity
AFTER INSERT OR UPDATE OR DELETE ON recipeweave.step_resource
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_recipe_integrity()
```

## database/migrations/002_relational_schema.sql:statement-1105

```sql
CREATE TRIGGER protect_recipe BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.step_media
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_recipe_content()
```

## database/migrations/002_relational_schema.sql:statement-1106

```sql
CREATE CONSTRAINT TRIGGER recipe_integrity
AFTER INSERT OR UPDATE OR DELETE ON recipeweave.step_media
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_recipe_integrity()
```

## database/migrations/002_relational_schema.sql:statement-1107

```sql
CREATE CONSTRAINT TRIGGER hierarchy_integrity AFTER INSERT OR UPDATE ON recipeweave.food
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_hierarchy()
```

## database/migrations/002_relational_schema.sql:statement-1108

```sql
CREATE CONSTRAINT TRIGGER hierarchy_integrity AFTER INSERT OR UPDATE ON recipeweave.axis_option
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_hierarchy()
```

## database/migrations/002_relational_schema.sql:statement-1109

```sql
CREATE CONSTRAINT TRIGGER cross_reference AFTER INSERT OR UPDATE ON recipeweave.product_version
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_cross_reference()
```

## database/migrations/002_relational_schema.sql:statement-1110

```sql
CREATE CONSTRAINT TRIGGER cross_reference AFTER INSERT OR UPDATE ON recipeweave.food_axis_option
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_cross_reference()
```

## database/migrations/002_relational_schema.sql:statement-1111

```sql
CREATE CONSTRAINT TRIGGER cross_reference AFTER INSERT OR UPDATE ON recipeweave.food_identity_member
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_cross_reference()
```

## database/migrations/002_relational_schema.sql:statement-1112

```sql
CREATE CONSTRAINT TRIGGER cross_reference AFTER INSERT OR UPDATE ON recipeweave.generation_choice
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_cross_reference()
```

## database/migrations/002_relational_schema.sql:statement-1113

```sql
CREATE CONSTRAINT TRIGGER cross_reference AFTER INSERT OR UPDATE ON recipeweave.generation_food
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_cross_reference()
```

## database/migrations/002_relational_schema.sql:statement-1114

```sql
CREATE CONSTRAINT TRIGGER cross_reference AFTER INSERT OR UPDATE ON recipeweave.generation_result
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_cross_reference()
```

## database/migrations/002_relational_schema.sql:statement-1115

```sql
CREATE CONSTRAINT TRIGGER cross_reference AFTER INSERT OR UPDATE ON recipeweave.generation_shard
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_cross_reference()
```

## database/migrations/002_relational_schema.sql:statement-1116

```sql
CREATE CONSTRAINT TRIGGER cross_reference AFTER INSERT OR UPDATE ON recipeweave.candidate_attempt
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_cross_reference()
```

## database/migrations/002_relational_schema.sql:statement-1117

```sql
CREATE CONSTRAINT TRIGGER cross_reference
AFTER INSERT OR UPDATE ON recipeweave.recipe_search_document
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_cross_reference()
```

## database/migrations/002_relational_schema.sql:statement-1118

```sql
CREATE TRIGGER protect_catalog BEFORE UPDATE OR DELETE ON recipeweave.catalog_release
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content()
```

## database/migrations/002_relational_schema.sql:statement-1119

```sql
CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.food
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content()
```

## database/migrations/002_relational_schema.sql:statement-1120

```sql
CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.food_alias
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content()
```

## database/migrations/002_relational_schema.sql:statement-1121

```sql
CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.food_form
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content()
```

## database/migrations/002_relational_schema.sql:statement-1122

```sql
CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.product
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content()
```

## database/migrations/002_relational_schema.sql:statement-1123

```sql
CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.food_identity_member
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content()
```

## database/migrations/002_relational_schema.sql:statement-1124

```sql
CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.food_axis_option
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content()
```

## database/migrations/002_relational_schema.sql:statement-1125

```sql
CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.axis
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content()
```

## database/migrations/002_relational_schema.sql:statement-1126

```sql
CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.axis_option
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content()
```

## database/migrations/002_relational_schema.sql:statement-1127

```sql
CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.food_allergen
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content()
```

## database/migrations/002_relational_schema.sql:statement-1128

```sql
CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.nutrition_fact
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content()
```

## database/migrations/002_relational_schema.sql:statement-1129

```sql
CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.product_version
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content()
```

## database/migrations/002_relational_schema.sql:statement-1130

```sql
CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.product_component
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content()
```

## database/migrations/002_relational_schema.sql:statement-1131

```sql
CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.product_allergen
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content()
```

## database/migrations/002_relational_schema.sql:statement-1132

```sql
CREATE TRIGGER protect_catalog
BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.product_preparation_rule
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content()
```

## database/migrations/002_relational_schema.sql:statement-1133

```sql
CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.conversion
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content()
```

## database/migrations/002_relational_schema.sql:statement-1134

```sql
CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.generation_policy
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content()
```

## database/migrations/002_relational_schema.sql:statement-1135

```sql
CREATE TRIGGER protect_catalog BEFORE INSERT OR UPDATE OR DELETE ON recipeweave.generation_template
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_catalog_content()
```

## database/migrations/002_relational_schema.sql:statement-1136

```sql
CREATE CONSTRAINT TRIGGER owned_integrity
AFTER INSERT OR UPDATE ON recipeweave.menu_ingredient_override
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_owned_reference()
```

## database/migrations/002_relational_schema.sql:statement-1137

```sql
CREATE CONSTRAINT TRIGGER owned_integrity AFTER INSERT OR UPDATE ON recipeweave.shopping_item
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_owned_reference()
```

## database/migrations/002_relational_schema.sql:statement-1138

```sql
CREATE CONSTRAINT TRIGGER owned_integrity AFTER INSERT OR UPDATE ON recipeweave.pantry_lot
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_owned_reference()
```

## database/migrations/002_relational_schema.sql:statement-1139

```sql
CREATE CONSTRAINT TRIGGER owned_integrity AFTER INSERT OR UPDATE ON recipeweave.session_task
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_owned_reference()
```

## database/migrations/002_relational_schema.sql:statement-1140

```sql
CREATE CONSTRAINT TRIGGER owned_integrity AFTER INSERT OR UPDATE ON recipeweave.cooking_session
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_owned_reference()
```

## database/migrations/002_relational_schema.sql:statement-1141

```sql
CREATE CONSTRAINT TRIGGER owned_integrity AFTER INSERT OR UPDATE ON recipeweave.task_dependency
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_owned_reference()
```

## database/migrations/002_relational_schema.sql:statement-1142

```sql
CREATE CONSTRAINT TRIGGER owned_integrity AFTER INSERT OR UPDATE ON recipeweave.resource_reservation
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_owned_reference()
```

## database/migrations/002_relational_schema.sql:statement-1143

```sql
CREATE TRIGGER execution_progress BEFORE UPDATE ON recipeweave.session_task
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_execution_progress()
```

## database/migrations/002_relational_schema.sql:statement-1144

```sql
CREATE TRIGGER execution_progress BEFORE UPDATE ON recipeweave.generation_shard
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_execution_progress()
```

## database/migrations/002_relational_schema.sql:statement-1145

```sql
CREATE TRIGGER audit_append_only BEFORE UPDATE OR DELETE ON recipeweave.audit_event
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_audit()
```

## database/migrations/002_relational_schema.sql:statement-1146

```sql
CREATE TRIGGER lifecycle_outbox AFTER INSERT OR UPDATE ON recipeweave.recipe_version
FOR EACH ROW EXECUTE FUNCTION recipeweave.publish_outbox()
```

## database/migrations/002_relational_schema.sql:statement-1147

```sql
CREATE TRIGGER lifecycle_outbox AFTER UPDATE ON recipeweave.recipe
FOR EACH ROW EXECUTE FUNCTION recipeweave.publish_outbox()
```

## database/migrations/002_relational_schema.sql:statement-1148

```sql
CREATE TRIGGER lifecycle_outbox AFTER DELETE ON recipeweave.app_user
FOR EACH ROW EXECUTE FUNCTION recipeweave.publish_outbox()
```

## database/migrations/002_relational_schema.sql:statement-1149

```sql
ALTER TABLE recipeweave.app_user ENABLE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1150

```sql
ALTER TABLE recipeweave.app_user FORCE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1151

```sql
CREATE POLICY owned_access ON recipeweave.app_user
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR app_user.id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR app_user.id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
```

## database/migrations/002_relational_schema.sql:statement-1152

```sql
ALTER TABLE recipeweave.user_preference ENABLE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1153

```sql
ALTER TABLE recipeweave.user_preference FORCE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1154

```sql
CREATE POLICY owned_access ON recipeweave.user_preference
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR user_preference.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR user_preference.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
```

## database/migrations/002_relational_schema.sql:statement-1155

```sql
ALTER TABLE recipeweave.user_exclusion ENABLE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1156

```sql
ALTER TABLE recipeweave.user_exclusion FORCE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1157

```sql
CREATE POLICY owned_access ON recipeweave.user_exclusion
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR user_exclusion.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR user_exclusion.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
```

## database/migrations/002_relational_schema.sql:statement-1158

```sql
ALTER TABLE recipeweave.user_recipe_event ENABLE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1159

```sql
ALTER TABLE recipeweave.user_recipe_event FORCE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1160

```sql
CREATE POLICY owned_access ON recipeweave.user_recipe_event
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR user_recipe_event.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR user_recipe_event.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
```

## database/migrations/002_relational_schema.sql:statement-1161

```sql
ALTER TABLE recipeweave.menu ENABLE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1162

```sql
ALTER TABLE recipeweave.menu FORCE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1163

```sql
CREATE POLICY owned_access ON recipeweave.menu
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR menu.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR menu.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
```

## database/migrations/002_relational_schema.sql:statement-1164

```sql
ALTER TABLE recipeweave.menu_item ENABLE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1165

```sql
ALTER TABLE recipeweave.menu_item FORCE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1166

```sql
CREATE POLICY owned_access ON recipeweave.menu_item
USING (
    CURRENT_SETTING(
        'recipeweave.role', TRUE) = 'admin' OR (
        SELECT r0.user_id FROM recipeweave.menu AS r0
        WHERE r0.id = menu_item.menu_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), ''
    )::UUID
) WITH CHECK (CURRENT_SETTING(
    'recipeweave.role', TRUE) = 'admin' OR (
    SELECT r0.user_id FROM recipeweave.menu AS r0
    WHERE r0.id = menu_item.menu_id
) = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), ''
)::UUID)
```

## database/migrations/002_relational_schema.sql:statement-1167

```sql
ALTER TABLE recipeweave.menu_ingredient_override ENABLE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1168

```sql
ALTER TABLE recipeweave.menu_ingredient_override FORCE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1169

```sql
CREATE POLICY owned_access ON recipeweave.menu_ingredient_override
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR (
        SELECT r1.user_id
        FROM recipeweave.menu_item AS r0
        INNER JOIN recipeweave.menu AS r1 ON r0.menu_id = r1.id
        WHERE r0.id = menu_ingredient_override.menu_item_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin' OR (
        SELECT r1.user_id
        FROM recipeweave.menu_item AS r0
        INNER JOIN recipeweave.menu AS r1 ON r0.menu_id = r1.id
        WHERE r0.id = menu_ingredient_override.menu_item_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
```

## database/migrations/002_relational_schema.sql:statement-1170

```sql
ALTER TABLE recipeweave.kitchen_resource ENABLE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1171

```sql
ALTER TABLE recipeweave.kitchen_resource FORCE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1172

```sql
CREATE POLICY owned_access ON recipeweave.kitchen_resource
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR kitchen_resource.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR kitchen_resource.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
```

## database/migrations/002_relational_schema.sql:statement-1173

```sql
ALTER TABLE recipeweave.cooking_session ENABLE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1174

```sql
ALTER TABLE recipeweave.cooking_session FORCE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1175

```sql
CREATE POLICY owned_access ON recipeweave.cooking_session
USING (
    CURRENT_SETTING(
        'recipeweave.role', TRUE) = 'admin' OR (
        SELECT r0.user_id FROM recipeweave.menu AS r0
        WHERE r0.id = cooking_session.menu_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), ''
    )::UUID
) WITH CHECK (CURRENT_SETTING(
    'recipeweave.role', TRUE) = 'admin' OR (
    SELECT r0.user_id FROM recipeweave.menu AS r0
    WHERE r0.id = cooking_session.menu_id
) = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), ''
)::UUID)
```

## database/migrations/002_relational_schema.sql:statement-1176

```sql
ALTER TABLE recipeweave.session_task ENABLE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1177

```sql
ALTER TABLE recipeweave.session_task FORCE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1178

```sql
CREATE POLICY owned_access ON recipeweave.session_task
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR (
        SELECT r1.user_id
        FROM recipeweave.cooking_session AS r0
        INNER JOIN recipeweave.menu AS r1 ON r0.menu_id = r1.id
        WHERE r0.id = session_task.session_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin' OR (
        SELECT r1.user_id
        FROM recipeweave.cooking_session AS r0
        INNER JOIN recipeweave.menu AS r1 ON r0.menu_id = r1.id
        WHERE r0.id = session_task.session_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
```

## database/migrations/002_relational_schema.sql:statement-1179

```sql
ALTER TABLE recipeweave.task_dependency ENABLE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1180

```sql
ALTER TABLE recipeweave.task_dependency FORCE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1181

```sql
CREATE POLICY owned_access ON recipeweave.task_dependency
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR (
        SELECT r2.user_id
        FROM recipeweave.session_task AS r0
        INNER JOIN recipeweave.cooking_session AS r1 ON r0.session_id = r1.id
        INNER JOIN recipeweave.menu AS r2 ON r1.menu_id = r2.id
        WHERE r0.id = task_dependency.before_task_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin' OR (
        SELECT r2.user_id
        FROM recipeweave.session_task AS r0
        INNER JOIN recipeweave.cooking_session AS r1 ON r0.session_id = r1.id
        INNER JOIN recipeweave.menu AS r2 ON r1.menu_id = r2.id
        WHERE r0.id = task_dependency.before_task_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
```

## database/migrations/002_relational_schema.sql:statement-1182

```sql
ALTER TABLE recipeweave.resource_reservation ENABLE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1183

```sql
ALTER TABLE recipeweave.resource_reservation FORCE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1184

```sql
CREATE POLICY owned_access ON recipeweave.resource_reservation
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR (
        SELECT r2.user_id
        FROM recipeweave.session_task AS r0
        INNER JOIN recipeweave.cooking_session AS r1 ON r0.session_id = r1.id
        INNER JOIN recipeweave.menu AS r2 ON r1.menu_id = r2.id
        WHERE r0.id = resource_reservation.task_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin' OR (
        SELECT r2.user_id
        FROM recipeweave.session_task AS r0
        INNER JOIN recipeweave.cooking_session AS r1 ON r0.session_id = r1.id
        INNER JOIN recipeweave.menu AS r2 ON r1.menu_id = r2.id
        WHERE r0.id = resource_reservation.task_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
```

## database/migrations/002_relational_schema.sql:statement-1185

```sql
ALTER TABLE recipeweave.ingredient_total ENABLE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1186

```sql
ALTER TABLE recipeweave.ingredient_total FORCE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1187

```sql
CREATE POLICY owned_access ON recipeweave.ingredient_total
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR (
        SELECT r1.user_id
        FROM recipeweave.cooking_session AS r0
        INNER JOIN recipeweave.menu AS r1 ON r0.menu_id = r1.id
        WHERE r0.id = ingredient_total.session_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin' OR (
        SELECT r1.user_id
        FROM recipeweave.cooking_session AS r0
        INNER JOIN recipeweave.menu AS r1 ON r0.menu_id = r1.id
        WHERE r0.id = ingredient_total.session_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
```

## database/migrations/002_relational_schema.sql:statement-1188

```sql
ALTER TABLE recipeweave.pantry_lot ENABLE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1189

```sql
ALTER TABLE recipeweave.pantry_lot FORCE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1190

```sql
CREATE POLICY owned_access ON recipeweave.pantry_lot
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR pantry_lot.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR pantry_lot.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
```

## database/migrations/002_relational_schema.sql:statement-1191

```sql
ALTER TABLE recipeweave.shopping_item ENABLE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1192

```sql
ALTER TABLE recipeweave.shopping_item FORCE ROW LEVEL SECURITY
```

## database/migrations/002_relational_schema.sql:statement-1193

```sql
CREATE POLICY owned_access ON recipeweave.shopping_item
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR (
        SELECT r1.user_id
        FROM recipeweave.cooking_session AS r0
        INNER JOIN recipeweave.menu AS r1 ON r0.menu_id = r1.id
        WHERE r0.id = shopping_item.session_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin' OR (
        SELECT r1.user_id
        FROM recipeweave.cooking_session AS r0
        INNER JOIN recipeweave.menu AS r1 ON r0.menu_id = r1.id
        WHERE r0.id = shopping_item.session_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
```

## database/migrations/002_relational_schema.sql:statement-1194

```sql
CREATE FUNCTION recipeweave.guard_adopted_definition() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
DECLARE
    reference record;
    referenced boolean;
BEGIN
    IF TG_OP = 'UPDATE' AND to_jsonb(OLD) ? 'status'
       AND (to_jsonb(NEW) - 'status') = (to_jsonb(OLD) - 'status') THEN RETURN NEW; END IF;
    FOR reference IN
        SELECT namespace.nspname AS schema_name, child.relname AS table_name, attribute.attname AS column_name
        FROM pg_constraint constraint_def
        JOIN pg_class child ON child.oid = constraint_def.conrelid
        JOIN pg_namespace namespace ON namespace.oid = child.relnamespace
        JOIN pg_attribute attribute ON attribute.attrelid = child.oid AND attribute.attnum = constraint_def.conkey[1]
        WHERE constraint_def.contype = 'f' AND constraint_def.confrelid = TG_RELID
          AND namespace.nspname = 'recipeweave' AND cardinality(constraint_def.conkey) = 1
    LOOP
        EXECUTE format('SELECT EXISTS (SELECT 1 FROM %I.%I WHERE %I = $1)',
            reference.schema_name, reference.table_name, reference.column_name) INTO referenced USING OLD.id;
        IF referenced THEN
            RAISE EXCEPTION '採用済みの定義版は変更・削除できません。新IDを作成してください' USING ERRCODE = '23514';
        END IF;
    END LOOP;
    RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
END;
$$
```

## database/migrations/002_relational_schema.sql:statement-1195

```sql
CREATE TRIGGER adopted_definition BEFORE UPDATE OR DELETE ON recipeweave.product_version
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_adopted_definition()
```

## database/migrations/002_relational_schema.sql:statement-1196

```sql
CREATE TRIGGER adopted_definition BEFORE UPDATE OR DELETE ON recipeweave.product_component
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_adopted_definition()
```

## database/migrations/002_relational_schema.sql:statement-1197

```sql
CREATE TRIGGER adopted_definition BEFORE UPDATE OR DELETE ON recipeweave.conversion
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_adopted_definition()
```

## database/migrations/002_relational_schema.sql:statement-1198

```sql
CREATE TRIGGER adopted_definition BEFORE UPDATE OR DELETE ON recipeweave.scaling_rule
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_adopted_definition()
```

## database/migrations/002_relational_schema.sql:statement-1199

```sql
CREATE TRIGGER adopted_definition BEFORE UPDATE OR DELETE ON recipeweave.media_asset
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_adopted_definition()
```

## database/migrations/002_relational_schema.sql:statement-1200

```sql
CREATE TRIGGER adopted_definition BEFORE UPDATE OR DELETE ON recipeweave.generation_policy
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_adopted_definition()
```

## database/migrations/002_relational_schema.sql:statement-1201

```sql
CREATE TRIGGER adopted_definition BEFORE UPDATE OR DELETE ON recipeweave.food_identity
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_adopted_definition()
```

## database/migrations/002_relational_schema.sql:statement-1202

```sql
CREATE TRIGGER adopted_definition BEFORE UPDATE OR DELETE ON recipeweave.generation_template
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_adopted_definition()
```

## database/migrations/002_relational_schema.sql:statement-1203

```sql
CREATE TRIGGER adopted_definition BEFORE UPDATE OR DELETE ON recipeweave.operation_parameter
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_adopted_definition()
```

## database/migrations/002_relational_schema.sql:statement-1204

```sql
CREATE TRIGGER adopted_definition BEFORE UPDATE OR DELETE ON recipeweave.unit
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_adopted_definition()
```

## database/migrations/002_relational_schema.sql:statement-1205

```sql
CREATE TRIGGER adopted_definition BEFORE UPDATE OR DELETE ON recipeweave.operation
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_adopted_definition()
```

## database/migrations/003_service_operations.sql:statement-52

```sql
ALTER TABLE recipeweave.recipe_version ADD COLUMN description TEXT
```

## database/migrations/003_service_operations.sql:statement-54

```sql
ALTER TABLE recipeweave.recipe_step ADD COLUMN title TEXT
```

## database/migrations/003_service_operations.sql:statement-56

```sql
ALTER TABLE recipeweave.recipe_ingredient ADD COLUMN note TEXT
```

## database/migrations/003_service_operations.sql:statement-58

```sql
ALTER TABLE recipeweave.pantry_lot ADD COLUMN location TEXT NOT NULL DEFAULT 'fridge'
```

## database/migrations/003_service_operations.sql:statement-60

```sql
ALTER TABLE recipeweave.pantry_lot ADD COLUMN priority TEXT NOT NULL DEFAULT 'normal'
```

## database/migrations/003_service_operations.sql:statement-62

```sql
ALTER TABLE recipeweave.pantry_lot ADD COLUMN status TEXT NOT NULL DEFAULT 'active'
```

## database/migrations/003_service_operations.sql:statement-64

```sql
ALTER TABLE recipeweave.pantry_lot ADD COLUMN source_import_id UUID
```

## database/migrations/003_service_operations.sql:statement-66

```sql
ALTER TABLE recipeweave.pantry_lot ADD COLUMN quantity_quality TEXT NOT NULL DEFAULT 'known'
```

## database/migrations/003_service_operations.sql:statement-68

```sql
ALTER TABLE recipeweave.pantry_lot ADD COLUMN original_form_id UUID
```

## database/migrations/003_service_operations.sql:statement-70

```sql
ALTER TABLE recipeweave.pantry_lot ADD COLUMN original_amount NUMERIC(20, 6)
```

## database/migrations/003_service_operations.sql:statement-72

```sql
ALTER TABLE recipeweave.pantry_lot ADD COLUMN original_unit_id UUID
```

## database/migrations/003_service_operations.sql:statement-74

```sql
ALTER TABLE recipeweave.pantry_lot ADD COLUMN updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
```

## database/migrations/003_service_operations.sql:statement-76

```sql
ALTER TABLE recipeweave.pantry_lot ADD COLUMN edited BOOLEAN NOT NULL DEFAULT FALSE
```

## database/migrations/003_service_operations.sql:statement-78

```sql
ALTER TABLE recipeweave.shopping_item ADD COLUMN client_key TEXT
```

## database/migrations/003_service_operations.sql:statement-80

```sql
ALTER TABLE recipeweave.shopping_item ADD COLUMN checked_at TIMESTAMPTZ
```

## database/migrations/003_service_operations.sql:statement-82

```sql
ALTER TABLE recipeweave.shopping_item ADD COLUMN archived BOOLEAN NOT NULL DEFAULT FALSE
```

## database/migrations/003_service_operations.sql:statement-84

```sql
ALTER TABLE recipeweave.pantry_lot ALTER COLUMN amount DROP NOT NULL
```

## database/migrations/003_service_operations.sql:statement-85

```sql
ALTER TABLE recipeweave.pantry_lot ADD CONSTRAINT pantry_location CHECK (
    location IN ('fridge', 'freezer', 'pantry')
)
```

## database/migrations/003_service_operations.sql:statement-86

```sql
ALTER TABLE recipeweave.pantry_lot ADD CONSTRAINT pantry_priority CHECK (
    priority IN ('normal', 'use_first')
)
```

## database/migrations/003_service_operations.sql:statement-87

```sql
ALTER TABLE recipeweave.pantry_lot ADD CONSTRAINT pantry_status CHECK (
    status IN ('active', 'deleted', 'undone')
)
```

## database/migrations/003_service_operations.sql:statement-88

```sql
ALTER TABLE recipeweave.pantry_lot ADD CONSTRAINT pantry_quantity CHECK (
    (quantity_quality = 'known' AND amount IS NOT NULL)
    OR (quantity_quality = 'unknown' AND amount IS NULL)
)
```

## database/migrations/003_service_operations.sql:statement-89

```sql
ALTER TABLE recipeweave.pantry_lot ADD CONSTRAINT pantry_original_amount CHECK (
    original_amount IS NULL
    OR (original_amount >= 0 AND original_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))
)
```

## database/migrations/003_service_operations.sql:statement-90

```sql
ALTER TABLE recipeweave.cooking_session DROP CONSTRAINT cooking_session_status_check
```

## database/migrations/003_service_operations.sql:statement-91

```sql
ALTER TABLE recipeweave.cooking_session ADD CONSTRAINT cooking_session_status_check CHECK (
    status IN ('planned', 'cooking', 'paused', 'completed', 'cancelled')
)
```

## database/migrations/003_service_operations.sql:statement-92

```sql
ALTER TABLE recipeweave.receipt_import ADD CONSTRAINT fk_receipt_import_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/003_service_operations.sql:statement-94

```sql
ALTER TABLE recipeweave.receipt_line ADD CONSTRAINT fk_receipt_line_import_id
FOREIGN KEY (import_id) REFERENCES recipeweave.receipt_import (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/003_service_operations.sql:statement-96

```sql
ALTER TABLE recipeweave.receipt_line ADD CONSTRAINT fk_receipt_line_form_id
FOREIGN KEY (form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/003_service_operations.sql:statement-98

```sql
ALTER TABLE recipeweave.receipt_line ADD CONSTRAINT fk_receipt_line_product_version_id
FOREIGN KEY (product_version_id) REFERENCES recipeweave.product_version (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/003_service_operations.sql:statement-100

```sql
ALTER TABLE recipeweave.receipt_line ADD CONSTRAINT fk_receipt_line_unit_id
FOREIGN KEY (unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/003_service_operations.sql:statement-102

```sql
ALTER TABLE recipeweave.receipt_line ADD CONSTRAINT fk_receipt_line_pantry_lot_id
FOREIGN KEY (pantry_lot_id) REFERENCES recipeweave.pantry_lot (id)
ON DELETE SET NULL ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/003_service_operations.sql:statement-104

```sql
ALTER TABLE recipeweave.workspace_revision ADD CONSTRAINT fk_workspace_revision_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/003_service_operations.sql:statement-106

```sql
ALTER TABLE recipeweave.user_food ADD CONSTRAINT fk_user_food_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/003_service_operations.sql:statement-108

```sql
ALTER TABLE recipeweave.user_food ADD CONSTRAINT fk_user_food_food_id
FOREIGN KEY (food_id) REFERENCES recipeweave.food (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/003_service_operations.sql:statement-110

```sql
ALTER TABLE recipeweave.user_pantry_food ADD CONSTRAINT fk_user_pantry_food_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/003_service_operations.sql:statement-112

```sql
ALTER TABLE recipeweave.user_pantry_food ADD CONSTRAINT fk_user_pantry_food_food_id
FOREIGN KEY (food_id) REFERENCES recipeweave.food (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/003_service_operations.sql:statement-114

```sql
ALTER TABLE recipeweave.pantry_consumption ADD CONSTRAINT fk_pantry_consumption_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/003_service_operations.sql:statement-116

```sql
ALTER TABLE recipeweave.pantry_consumption ADD CONSTRAINT fk_pantry_consumption_session_id
FOREIGN KEY (session_id) REFERENCES recipeweave.cooking_session (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/003_service_operations.sql:statement-118

```sql
ALTER TABLE recipeweave.pantry_consumption ADD CONSTRAINT fk_pantry_consumption_lot_id
FOREIGN KEY (lot_id) REFERENCES recipeweave.pantry_lot (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/003_service_operations.sql:statement-120

```sql
ALTER TABLE recipeweave.pantry_consumption ADD CONSTRAINT fk_pantry_consumption_unit_id
FOREIGN KEY (unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/003_service_operations.sql:statement-122

```sql
ALTER TABLE recipeweave.pantry_lot ADD CONSTRAINT fk_pantry_lot_source_import_id
FOREIGN KEY (source_import_id) REFERENCES recipeweave.receipt_import (id)
ON DELETE SET NULL ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/003_service_operations.sql:statement-124

```sql
ALTER TABLE recipeweave.pantry_lot ADD CONSTRAINT fk_pantry_lot_original_form_id
FOREIGN KEY (original_form_id) REFERENCES recipeweave.food_form (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/003_service_operations.sql:statement-126

```sql
ALTER TABLE recipeweave.pantry_lot ADD CONSTRAINT fk_pantry_lot_original_unit_id
FOREIGN KEY (original_unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/003_service_operations.sql:statement-128

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.receipt_import
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/003_service_operations.sql:statement-129

```sql
ALTER TABLE recipeweave.receipt_import ENABLE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-130

```sql
ALTER TABLE recipeweave.receipt_import FORCE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-131

```sql
CREATE POLICY owned_access ON recipeweave.receipt_import
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR receipt_import.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR receipt_import.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
```

## database/migrations/003_service_operations.sql:statement-132

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.receipt_line
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/003_service_operations.sql:statement-133

```sql
ALTER TABLE recipeweave.receipt_line ENABLE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-134

```sql
ALTER TABLE recipeweave.receipt_line FORCE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-135

```sql
CREATE POLICY owned_access ON recipeweave.receipt_line
USING (
    CURRENT_SETTING(
        'recipeweave.role', TRUE
    ) = 'admin'
    OR (
        SELECT r.user_id FROM recipeweave.receipt_import AS r
        WHERE r.id = receipt_line.import_id
    ) = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), ''
    )::UUID
) WITH CHECK (CURRENT_SETTING(
    'recipeweave.role', TRUE) = 'admin' OR (
    SELECT r.user_id FROM recipeweave.receipt_import AS r
    WHERE r.id = receipt_line.import_id
) = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), ''
)::UUID)
```

## database/migrations/003_service_operations.sql:statement-136

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.workspace_revision
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/003_service_operations.sql:statement-137

```sql
ALTER TABLE recipeweave.workspace_revision ENABLE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-138

```sql
ALTER TABLE recipeweave.workspace_revision FORCE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-139

```sql
CREATE POLICY owned_access ON recipeweave.workspace_revision
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR workspace_revision.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR workspace_revision.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
```

## database/migrations/003_service_operations.sql:statement-140

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.user_food
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/003_service_operations.sql:statement-141

```sql
ALTER TABLE recipeweave.user_food ENABLE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-142

```sql
ALTER TABLE recipeweave.user_food FORCE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-143

```sql
CREATE POLICY owned_access ON recipeweave.user_food
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR user_food.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR user_food.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
```

## database/migrations/003_service_operations.sql:statement-144

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.user_pantry_food
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/003_service_operations.sql:statement-145

```sql
ALTER TABLE recipeweave.user_pantry_food ENABLE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-146

```sql
ALTER TABLE recipeweave.user_pantry_food FORCE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-147

```sql
CREATE POLICY owned_access ON recipeweave.user_pantry_food
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR user_pantry_food.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR user_pantry_food.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
```

## database/migrations/003_service_operations.sql:statement-148

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.pantry_consumption
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/003_service_operations.sql:statement-149

```sql
ALTER TABLE recipeweave.pantry_consumption ENABLE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-150

```sql
ALTER TABLE recipeweave.pantry_consumption FORCE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-151

```sql
CREATE POLICY owned_access ON recipeweave.pantry_consumption
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR pantry_consumption.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR pantry_consumption.user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
```

## database/migrations/003_service_operations.sql:statement-164

```sql
ALTER TABLE recipeweave.user_shopping_check ADD CONSTRAINT fk_user_shopping_check_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE CASCADE ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/003_service_operations.sql:statement-165

```sql
ALTER TABLE recipeweave.user_shopping_check ADD CONSTRAINT fk_user_shopping_check_food_id
FOREIGN KEY (food_id) REFERENCES recipeweave.food (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/003_service_operations.sql:statement-166

```sql
ALTER TABLE recipeweave.user_shopping_check ADD CONSTRAINT fk_user_shopping_check_unit_id
FOREIGN KEY (unit_id) REFERENCES recipeweave.unit (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/003_service_operations.sql:statement-170

```sql
CREATE TRIGGER immutable_id BEFORE UPDATE ON recipeweave.user_shopping_check
FOR EACH ROW EXECUTE FUNCTION recipeweave.reject_identity_change()
```

## database/migrations/003_service_operations.sql:statement-171

```sql
ALTER TABLE recipeweave.user_shopping_check ENABLE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-172

```sql
ALTER TABLE recipeweave.user_shopping_check FORCE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-173

```sql
CREATE POLICY owned_access ON recipeweave.user_shopping_check
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
```

## database/migrations/003_service_operations.sql:statement-174

```sql
CREATE FUNCTION recipeweave.check_receipt_reference() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
DECLARE
    v_import_id uuid;
    current_import recipeweave.receipt_import%ROWTYPE;
    current_lot recipeweave.pantry_lot%ROWTYPE;
BEGIN

    EXECUTE format('SELECT * FROM recipeweave.%I WHERE id = $1', TG_TABLE_NAME) INTO NEW USING NEW.id;
    IF NEW.id IS NULL THEN RETURN NULL; END IF;
    IF TG_TABLE_NAME = 'receipt_import' THEN
        v_import_id := NEW.id;
    ELSIF TG_TABLE_NAME = 'receipt_line' THEN
        v_import_id := NEW.import_id;
        IF NEW.pantry_lot_id IS NOT NULL THEN
            SELECT * INTO current_lot FROM recipeweave.pantry_lot WHERE id = NEW.pantry_lot_id;
            SELECT * INTO current_import FROM recipeweave.receipt_import WHERE id = v_import_id;
            IF current_lot.user_id <> current_import.user_id OR current_lot.source_import_id IS DISTINCT FROM v_import_id
               OR current_lot.form_id IS DISTINCT FROM NEW.form_id THEN
                RAISE EXCEPTION 'レシート行と在庫ロットの所有者・登録元・食材が不一致です' USING ERRCODE = '23514';
            END IF;
        END IF;
        IF NEW.product_version_id IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM recipeweave.product_version WHERE id = NEW.product_version_id AND form_id = NEW.form_id
        ) THEN RAISE EXCEPTION 'レシートの商品と食材形態が不一致です' USING ERRCODE = '23514'; END IF;
    ELSIF TG_TABLE_NAME = 'pantry_lot' THEN
        v_import_id := NEW.source_import_id;
        IF v_import_id IS NULL THEN RETURN NULL; END IF;
        IF NOT EXISTS (SELECT 1 FROM recipeweave.receipt_import WHERE id = v_import_id AND user_id = NEW.user_id) THEN
            RAISE EXCEPTION '他人のレシートへ在庫を紐付けできません' USING ERRCODE = '23514';
        END IF;
    END IF;
    SELECT * INTO current_import FROM recipeweave.receipt_import WHERE id = v_import_id FOR UPDATE;
    IF NOT FOUND THEN RETURN NULL; END IF;
    IF current_import.status = 'committed' AND EXISTS (
        SELECT 1 FROM recipeweave.receipt_line line WHERE line.import_id = v_import_id
        AND (line.decision = 'unresolved' OR (line.decision = 'accepted' AND line.pantry_lot_id IS NULL))
    ) THEN RAISE EXCEPTION '未解決または未登録のレシート行が残っています' USING ERRCODE = '23514'; END IF;
    IF current_import.status = 'reverted' AND EXISTS (
        SELECT 1 FROM recipeweave.pantry_lot lot WHERE lot.source_import_id = v_import_id AND lot.status = 'active'
        AND NOT lot.edited AND NOT EXISTS (SELECT 1 FROM recipeweave.pantry_consumption c WHERE c.lot_id = lot.id)
    ) THEN RAISE EXCEPTION '取消後のレシートに未編集・未消費の有効な在庫が残っています' USING ERRCODE = '23514'; END IF;
    RETURN NULL;
END;
$$
```

## database/migrations/003_service_operations.sql:statement-175

```sql
CREATE FUNCTION recipeweave.guard_receipt_lifecycle() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN
    IF OLD.user_id <> NEW.user_id OR OLD.idempotency_key <> NEW.idempotency_key
       OR NEW.revision <= OLD.revision
       OR (OLD.status = 'reverted' AND NEW.status <> 'reverted')
       OR (OLD.status = 'committed' AND NEW.status = 'draft') THEN
        RAISE EXCEPTION 'レシートの状態・所有者・版の遷移が不正です' USING ERRCODE = '23514';
    END IF;
    IF NEW.status = 'reverted' THEN
        SELECT COUNT(*) INTO NEW.undo_preserved_count FROM recipeweave.pantry_lot lot
        WHERE lot.source_import_id = OLD.id AND lot.status = 'active'
        AND (lot.edited OR EXISTS (SELECT 1 FROM recipeweave.pantry_consumption c WHERE c.lot_id = lot.id));
    END IF;
    RETURN NEW;
END;
$$
```

## database/migrations/003_service_operations.sql:statement-176

```sql
CREATE FUNCTION recipeweave.check_consumption_owner() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN

    EXECUTE format('SELECT * FROM recipeweave.%I WHERE id = $1', TG_TABLE_NAME) INTO NEW USING NEW.id;
    IF NEW.id IS NULL THEN RETURN NULL; END IF;
    IF NOT EXISTS (
        SELECT 1 FROM recipeweave.pantry_lot lot, recipeweave.cooking_session session
        JOIN recipeweave.menu menu ON menu.id = session.menu_id
        WHERE lot.id = NEW.lot_id AND lot.user_id = NEW.user_id AND lot.unit_id = NEW.unit_id
        AND session.id = NEW.session_id AND menu.user_id = NEW.user_id
    ) THEN RAISE EXCEPTION '消費元と調理の所有者・単位が不一致です' USING ERRCODE = '23514'; END IF;
    RETURN NULL;
END;
$$
```

## database/migrations/003_service_operations.sql:statement-177

```sql
CREATE CONSTRAINT TRIGGER receipt_integrity AFTER INSERT OR UPDATE ON recipeweave.receipt_import
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_receipt_reference()
```

## database/migrations/003_service_operations.sql:statement-178

```sql
CREATE CONSTRAINT TRIGGER receipt_integrity AFTER INSERT OR UPDATE ON recipeweave.receipt_line
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_receipt_reference()
```

## database/migrations/003_service_operations.sql:statement-179

```sql
CREATE CONSTRAINT TRIGGER receipt_integrity AFTER INSERT OR UPDATE ON recipeweave.pantry_lot
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_receipt_reference()
```

## database/migrations/003_service_operations.sql:statement-180

```sql
CREATE TRIGGER receipt_lifecycle BEFORE UPDATE ON recipeweave.receipt_import
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_receipt_lifecycle()
```

## database/migrations/003_service_operations.sql:statement-181

```sql
CREATE CONSTRAINT TRIGGER consumption_owner AFTER INSERT OR UPDATE ON recipeweave.pantry_consumption
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_consumption_owner()
```

## database/migrations/003_service_operations.sql:statement-183

```sql
REVOKE INSERT, UPDATE, DELETE ON recipeweave.user_state FROM public
```

## database/migrations/003_service_operations.sql:statement-184

```sql
ALTER TABLE recipeweave.food ADD COLUMN owner_id UUID
```

## database/migrations/003_service_operations.sql:statement-186

```sql
ALTER TABLE recipeweave.food ADD CONSTRAINT fk_food_owner_id
FOREIGN KEY (owner_id) REFERENCES recipeweave.app_user (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/003_service_operations.sql:statement-188

```sql
ALTER TABLE recipeweave.food ENABLE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-189

```sql
ALTER TABLE recipeweave.food FORCE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-190

```sql
CREATE POLICY food_read ON recipeweave.food FOR SELECT
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin' OR owner_id IS NULL
    OR owner_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
```

## database/migrations/003_service_operations.sql:statement-191

```sql
CREATE POLICY food_write ON recipeweave.food FOR ALL
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR owner_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR owner_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
```

## database/migrations/003_service_operations.sql:statement-192

```sql
CREATE FUNCTION recipeweave.food_visible(food_id UUID) RETURNS BOOLEAN
LANGUAGE sql STABLE SET search_path = pg_catalog, recipeweave AS $$
    SELECT EXISTS (SELECT 1 FROM recipeweave.food WHERE id = food_id);
$$
```

## database/migrations/003_service_operations.sql:statement-193

```sql
CREATE FUNCTION recipeweave.food_writable(food_id UUID) RETURNS BOOLEAN
LANGUAGE sql STABLE SET search_path = pg_catalog, recipeweave AS $$
    SELECT current_setting('recipeweave.role', true) = 'admin' OR EXISTS (
        SELECT 1 FROM recipeweave.food WHERE id = food_id
        AND owner_id = nullif(current_setting('recipeweave.user_id', true), '')::uuid
    );
$$
```

## database/migrations/003_service_operations.sql:statement-194

```sql
CREATE FUNCTION recipeweave.check_private_food_owner() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN

    EXECUTE format('SELECT * FROM recipeweave.%I WHERE id = $1', TG_TABLE_NAME) INTO NEW USING NEW.id;
    IF NEW.id IS NULL THEN RETURN NULL; END IF;
    IF TG_TABLE_NAME = 'user_food' AND NOT EXISTS (
        SELECT 1 FROM recipeweave.food WHERE id = NEW.food_id AND owner_id = NEW.user_id
    ) THEN RAISE EXCEPTION '独自食材と所有者が一致しません' USING ERRCODE = '23514'; END IF;
    RETURN NULL;
END;
$$
```

## database/migrations/003_service_operations.sql:statement-195

```sql
CREATE CONSTRAINT TRIGGER private_food_owner AFTER INSERT OR UPDATE ON recipeweave.user_food
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_private_food_owner()
```

## database/migrations/003_service_operations.sql:statement-196

```sql
ALTER TABLE recipeweave.food_form ENABLE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-197

```sql
ALTER TABLE recipeweave.food_form FORCE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-198

```sql
CREATE POLICY food_derived_read ON recipeweave.food_form FOR SELECT
USING (recipeweave.food_visible(food_id))
```

## database/migrations/003_service_operations.sql:statement-199

```sql
CREATE POLICY food_derived_write ON recipeweave.food_form FOR ALL
USING (recipeweave.food_writable(food_id)) WITH CHECK (recipeweave.food_writable(food_id))
```

## database/migrations/003_service_operations.sql:statement-200

```sql
ALTER TABLE recipeweave.food_alias ENABLE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-201

```sql
ALTER TABLE recipeweave.food_alias FORCE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-202

```sql
CREATE POLICY food_derived_read ON recipeweave.food_alias FOR SELECT
USING (recipeweave.food_visible(food_id))
```

## database/migrations/003_service_operations.sql:statement-203

```sql
CREATE POLICY food_derived_write ON recipeweave.food_alias FOR ALL
USING (recipeweave.food_writable(food_id)) WITH CHECK (recipeweave.food_writable(food_id))
```

## database/migrations/003_service_operations.sql:statement-204

```sql
ALTER TABLE recipeweave.food_axis_option ENABLE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-205

```sql
ALTER TABLE recipeweave.food_axis_option FORCE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-206

```sql
CREATE POLICY food_derived_read ON recipeweave.food_axis_option FOR SELECT
USING (recipeweave.food_visible(food_id))
```

## database/migrations/003_service_operations.sql:statement-207

```sql
CREATE POLICY food_derived_write ON recipeweave.food_axis_option FOR ALL
USING (recipeweave.food_writable(food_id)) WITH CHECK (recipeweave.food_writable(food_id))
```

## database/migrations/003_service_operations.sql:statement-208

```sql
ALTER TABLE recipeweave.product ENABLE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-209

```sql
ALTER TABLE recipeweave.product FORCE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-210

```sql
CREATE POLICY food_derived_read ON recipeweave.product FOR SELECT
USING (recipeweave.food_visible(food_id))
```

## database/migrations/003_service_operations.sql:statement-211

```sql
CREATE POLICY food_derived_write ON recipeweave.product FOR ALL
USING (recipeweave.food_writable(food_id)) WITH CHECK (recipeweave.food_writable(food_id))
```

## database/migrations/003_service_operations.sql:statement-212

```sql
ALTER TABLE recipeweave.conversion ENABLE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-213

```sql
ALTER TABLE recipeweave.conversion FORCE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-214

```sql
CREATE POLICY food_derived_read ON recipeweave.conversion FOR SELECT
USING (
    recipeweave.food_visible((
        SELECT food_form.food_id FROM recipeweave.food_form
        WHERE food_form.id = conversion.form_id
    ))
)
```

## database/migrations/003_service_operations.sql:statement-215

```sql
CREATE POLICY food_derived_write ON recipeweave.conversion FOR ALL
USING (
    recipeweave.food_writable((
        SELECT food_form.food_id FROM recipeweave.food_form
        WHERE food_form.id = conversion.form_id
    ))
) WITH CHECK (recipeweave.food_writable((
    SELECT food_form.food_id FROM recipeweave.food_form
    WHERE food_form.id = conversion.form_id
)))
```

## database/migrations/003_service_operations.sql:statement-216

```sql
ALTER TABLE recipeweave.food_allergen ENABLE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-217

```sql
ALTER TABLE recipeweave.food_allergen FORCE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-218

```sql
CREATE POLICY food_derived_read ON recipeweave.food_allergen FOR SELECT
USING (
    recipeweave.food_visible((
        SELECT food_form.food_id FROM recipeweave.food_form
        WHERE food_form.id = food_allergen.form_id
    ))
)
```

## database/migrations/003_service_operations.sql:statement-219

```sql
CREATE POLICY food_derived_write ON recipeweave.food_allergen FOR ALL
USING (
    recipeweave.food_writable((
        SELECT food_form.food_id FROM recipeweave.food_form
        WHERE food_form.id = food_allergen.form_id
    ))
) WITH CHECK (recipeweave.food_writable((
    SELECT food_form.food_id FROM recipeweave.food_form
    WHERE food_form.id = food_allergen.form_id
)))
```

## database/migrations/003_service_operations.sql:statement-220

```sql
ALTER TABLE recipeweave.product_version ENABLE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-221

```sql
ALTER TABLE recipeweave.product_version FORCE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-222

```sql
CREATE POLICY food_derived_read ON recipeweave.product_version FOR SELECT
USING (
    recipeweave.food_visible((
        SELECT product.food_id FROM recipeweave.product
        WHERE product.id = product_version.product_id
    ))
)
```

## database/migrations/003_service_operations.sql:statement-223

```sql
CREATE POLICY food_derived_write ON recipeweave.product_version FOR ALL
USING (
    recipeweave.food_writable((
        SELECT product.food_id FROM recipeweave.product
        WHERE product.id = product_version.product_id
    ))
) WITH CHECK (recipeweave.food_writable((
    SELECT product.food_id FROM recipeweave.product
    WHERE product.id = product_version.product_id
)))
```

## database/migrations/003_service_operations.sql:statement-224

```sql
ALTER TABLE recipeweave.product_component ENABLE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-225

```sql
ALTER TABLE recipeweave.product_component FORCE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-226

```sql
CREATE POLICY food_derived_read ON recipeweave.product_component FOR SELECT
USING (
    recipeweave.food_visible(
        (
            SELECT product.food_id
            FROM recipeweave.product_version AS version
            INNER JOIN recipeweave.product AS product ON version.product_id = product.id
            WHERE version.id = product_component.product_version_id
        )
    )
)
```

## database/migrations/003_service_operations.sql:statement-227

```sql
CREATE POLICY food_derived_write ON recipeweave.product_component FOR ALL
USING (
    recipeweave.food_writable(
        (
            SELECT product.food_id
            FROM recipeweave.product_version AS version
            INNER JOIN recipeweave.product AS product ON version.product_id = product.id
            WHERE version.id = product_component.product_version_id
        )
    )
) WITH CHECK (
    recipeweave.food_writable((
        SELECT product.food_id
        FROM recipeweave.product_version AS version
        INNER JOIN recipeweave.product AS product ON version.product_id = product.id
        WHERE version.id = product_component.product_version_id
    ))
)
```

## database/migrations/003_service_operations.sql:statement-228

```sql
ALTER TABLE recipeweave.product_allergen ENABLE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-229

```sql
ALTER TABLE recipeweave.product_allergen FORCE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-230

```sql
CREATE POLICY food_derived_read ON recipeweave.product_allergen FOR SELECT
USING (
    recipeweave.food_visible(
        (
            SELECT product.food_id
            FROM recipeweave.product_version AS version
            INNER JOIN recipeweave.product AS product ON version.product_id = product.id
            WHERE version.id = product_allergen.product_version_id
        )
    )
)
```

## database/migrations/003_service_operations.sql:statement-231

```sql
CREATE POLICY food_derived_write ON recipeweave.product_allergen FOR ALL
USING (
    recipeweave.food_writable(
        (
            SELECT product.food_id
            FROM recipeweave.product_version AS version
            INNER JOIN recipeweave.product AS product ON version.product_id = product.id
            WHERE version.id = product_allergen.product_version_id
        )
    )
) WITH CHECK (
    recipeweave.food_writable((
        SELECT product.food_id
        FROM recipeweave.product_version AS version
        INNER JOIN recipeweave.product AS product ON version.product_id = product.id
        WHERE version.id = product_allergen.product_version_id
    ))
)
```

## database/migrations/003_service_operations.sql:statement-232

```sql
ALTER TABLE recipeweave.product_preparation_rule ENABLE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-233

```sql
ALTER TABLE recipeweave.product_preparation_rule FORCE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-234

```sql
CREATE POLICY food_derived_read ON recipeweave.product_preparation_rule FOR SELECT
USING (
    recipeweave.food_visible(
        (
            SELECT product.food_id
            FROM recipeweave.product_version AS version
            INNER JOIN recipeweave.product AS product ON version.product_id = product.id
            WHERE version.id = product_preparation_rule.product_version_id
        )
    )
)
```

## database/migrations/003_service_operations.sql:statement-235

```sql
CREATE POLICY food_derived_write ON recipeweave.product_preparation_rule FOR ALL
USING (
    recipeweave.food_writable(
        (
            SELECT product.food_id
            FROM recipeweave.product_version AS version
            INNER JOIN recipeweave.product AS product ON version.product_id = product.id
            WHERE version.id = product_preparation_rule.product_version_id
        )
    )
) WITH CHECK (
    recipeweave.food_writable((
        SELECT product.food_id
        FROM recipeweave.product_version AS version
        INNER JOIN recipeweave.product AS product ON version.product_id = product.id
        WHERE version.id = product_preparation_rule.product_version_id
    ))
)
```

## database/migrations/003_service_operations.sql:statement-236

```sql
ALTER TABLE recipeweave.nutrition_fact ENABLE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-237

```sql
ALTER TABLE recipeweave.nutrition_fact FORCE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-238

```sql
CREATE POLICY food_derived_read ON recipeweave.nutrition_fact FOR SELECT
USING (
    recipeweave.food_visible(COALESCE((
        SELECT food_form.food_id FROM recipeweave.food_form
        WHERE food_form.id = nutrition_fact.form_id
    ),
    (
        SELECT product.food_id
        FROM recipeweave.product_version AS version
        INNER JOIN recipeweave.product AS product ON version.product_id = product.id
        WHERE version.id = nutrition_fact.product_version_id
    )))
)
```

## database/migrations/003_service_operations.sql:statement-239

```sql
CREATE POLICY food_derived_write ON recipeweave.nutrition_fact FOR ALL
USING (
    recipeweave.food_writable(COALESCE((
        SELECT food_form.food_id FROM recipeweave.food_form
        WHERE food_form.id = nutrition_fact.form_id
    ),
    (
        SELECT product.food_id
        FROM recipeweave.product_version AS version
        INNER JOIN recipeweave.product AS product ON version.product_id = product.id
        WHERE version.id = nutrition_fact.product_version_id
    )))
) WITH CHECK (recipeweave.food_writable(COALESCE((
    SELECT food_form.food_id FROM recipeweave.food_form
    WHERE food_form.id = nutrition_fact.form_id
),
(
    SELECT product.food_id
    FROM recipeweave.product_version AS version
    INNER JOIN recipeweave.product AS product ON version.product_id = product.id
    WHERE version.id = nutrition_fact.product_version_id
))))
```

## database/migrations/003_service_operations.sql:statement-240

```sql
ALTER TABLE recipeweave.form_yield ENABLE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-241

```sql
ALTER TABLE recipeweave.form_yield FORCE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-242

```sql
CREATE POLICY food_derived_read ON recipeweave.form_yield FOR SELECT
USING (
    recipeweave.food_visible((
        SELECT food_form.food_id FROM recipeweave.food_form
        WHERE food_form.id = form_yield.input_form_id
    ))
)
```

## database/migrations/003_service_operations.sql:statement-243

```sql
CREATE POLICY food_derived_write ON recipeweave.form_yield FOR ALL
USING (
    recipeweave.food_writable((
        SELECT food_form.food_id FROM recipeweave.food_form
        WHERE food_form.id = form_yield.input_form_id
    ))
) WITH CHECK (recipeweave.food_writable((
    SELECT food_form.food_id FROM recipeweave.food_form
    WHERE food_form.id = form_yield.input_form_id
)))
```

## database/migrations/003_service_operations.sql:statement-244

```sql
ALTER TABLE recipeweave.cooking_session ADD COLUMN current_task_index INTEGER NOT NULL DEFAULT 0
```

## database/migrations/003_service_operations.sql:statement-246

```sql
ALTER TABLE recipeweave.cooking_session ADD CONSTRAINT cooking_current_index CHECK (
    current_task_index >= 0
)
```

## database/migrations/003_service_operations.sql:statement-247

```sql
ALTER TABLE recipeweave.session_task ADD COLUMN timer_started_at TIMESTAMPTZ
```

## database/migrations/003_service_operations.sql:statement-249

```sql
ALTER TABLE recipeweave.session_task ADD COLUMN timer_duration_s INTEGER
```

## database/migrations/003_service_operations.sql:statement-251

```sql
ALTER TABLE recipeweave.session_task ADD CONSTRAINT timer_duration CHECK (
    timer_duration_s IS NULL OR timer_duration_s >= 0
)
```

## database/migrations/003_service_operations.sql:statement-252

```sql
ALTER TABLE recipeweave.session_task ADD CONSTRAINT timer_start_requires_duration CHECK (
    timer_started_at IS NULL OR timer_duration_s IS NOT NULL
)
```

## database/migrations/003_service_operations.sql:statement-253

```sql
ALTER TABLE recipeweave.ingredient_total ADD COLUMN actual_amount NUMERIC(20, 6)
```

## database/migrations/003_service_operations.sql:statement-255

```sql
ALTER TABLE recipeweave.ingredient_total
ADD COLUMN consumption_outcome TEXT NOT NULL DEFAULT 'not_requested'
```

## database/migrations/003_service_operations.sql:statement-257

```sql
ALTER TABLE recipeweave.ingredient_total ADD CONSTRAINT actual_amount_finite CHECK (
    actual_amount IS NULL
    OR (actual_amount >= 0 AND actual_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))
)
```

## database/migrations/003_service_operations.sql:statement-258

```sql
ALTER TABLE recipeweave.ingredient_total ADD CONSTRAINT consumption_outcome_values CHECK (
    consumption_outcome IN ('not_requested', 'applied', 'insufficient', 'unknown', 'incompatible')
)
```

## database/migrations/003_service_operations.sql:statement-259

```sql
ALTER TABLE recipeweave.kitchen_resource ADD COLUMN active BOOLEAN NOT NULL DEFAULT TRUE
```

## database/migrations/003_service_operations.sql:statement-261

```sql
ALTER TABLE recipeweave.receipt_import ADD COLUMN undo_preserved_count INTEGER NOT NULL DEFAULT 0
```

## database/migrations/003_service_operations.sql:statement-263

```sql
ALTER TABLE recipeweave.receipt_import ADD CONSTRAINT undo_preserved_count_nonnegative CHECK (
    undo_preserved_count >= 0
)
```

## database/migrations/003_service_operations.sql:statement-264

```sql
ALTER TABLE recipeweave.catalog_release ADD COLUMN owner_id UUID
```

## database/migrations/003_service_operations.sql:statement-266

```sql
ALTER TABLE recipeweave.catalog_release ADD CONSTRAINT fk_catalog_release_owner_id
FOREIGN KEY (owner_id) REFERENCES recipeweave.app_user (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/003_service_operations.sql:statement-268

```sql
ALTER TABLE recipeweave.catalog_release ADD CONSTRAINT private_catalog_unpublished CHECK (
    owner_id IS NULL OR published_at IS NULL
)
```

## database/migrations/003_service_operations.sql:statement-269

```sql
ALTER TABLE recipeweave.catalog_release ENABLE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-270

```sql
ALTER TABLE recipeweave.catalog_release FORCE ROW LEVEL SECURITY
```

## database/migrations/003_service_operations.sql:statement-271

```sql
CREATE POLICY catalog_read ON recipeweave.catalog_release FOR SELECT
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin' OR owner_id IS NULL
    OR owner_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
```

## database/migrations/003_service_operations.sql:statement-272

```sql
CREATE POLICY catalog_write ON recipeweave.catalog_release FOR ALL
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR owner_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR owner_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
```

## database/migrations/003_service_operations.sql:statement-273

```sql
CREATE FUNCTION recipeweave.guard_private_owner() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.owner_id IS DISTINCT FROM OLD.owner_id THEN
        RAISE EXCEPTION '所有者の付替えや私有データの共通公開への変更はできません' USING ERRCODE = '23514';
    END IF;
    RETURN NEW;
END;
$$
```

## database/migrations/003_service_operations.sql:statement-274

```sql
CREATE TRIGGER private_owner_immutable BEFORE UPDATE ON recipeweave.food
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_private_owner()
```

## database/migrations/003_service_operations.sql:statement-275

```sql
CREATE TRIGGER private_owner_immutable BEFORE UPDATE ON recipeweave.catalog_release
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_private_owner()
```

## database/migrations/003_service_operations.sql:statement-276

```sql
CREATE FUNCTION recipeweave.check_food_release_owner() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
DECLARE
    catalog_owner uuid;
BEGIN
    SELECT owner_id INTO catalog_owner FROM recipeweave.catalog_release WHERE id = NEW.release_id;
    IF catalog_owner IS DISTINCT FROM NEW.owner_id THEN
        RAISE EXCEPTION '食材と所属カタログの所有者が一致しません' USING ERRCODE = '23514';
    END IF;
    RETURN NULL;
END;
$$
```

## database/migrations/003_service_operations.sql:statement-277

```sql
CREATE CONSTRAINT TRIGGER food_release_owner AFTER INSERT OR UPDATE ON recipeweave.food
DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION recipeweave.check_food_release_owner()
```

## database/migrations/003_service_operations.sql:statement-278

```sql
ALTER TABLE recipeweave.food
ADD CONSTRAINT food_name_wire_length CHECK (CHAR_LENGTH(name) <= 100)
```

## database/migrations/003_service_operations.sql:statement-279

```sql
ALTER TABLE recipeweave.food_alias
ADD CONSTRAINT food_alias_alias_wire_length CHECK (CHAR_LENGTH(alias) <= 500)
```

## database/migrations/003_service_operations.sql:statement-280

```sql
ALTER TABLE recipeweave.food_form
ADD CONSTRAINT food_form_name_wire_length CHECK (CHAR_LENGTH(name) <= 500)
```

## database/migrations/003_service_operations.sql:statement-281

```sql
ALTER TABLE recipeweave.recipe
ADD CONSTRAINT recipe_title_wire_length CHECK (CHAR_LENGTH(title) <= 500)
```

## database/migrations/003_service_operations.sql:statement-282

```sql
ALTER TABLE recipeweave.recipe_version
ADD CONSTRAINT recipe_version_description_wire_length CHECK (CHAR_LENGTH(description) <= 5000)
```

## database/migrations/003_service_operations.sql:statement-283

```sql
ALTER TABLE recipeweave.recipe_step
ADD CONSTRAINT recipe_step_title_wire_length CHECK (CHAR_LENGTH(title) <= 500)
```

## database/migrations/003_service_operations.sql:statement-284

```sql
ALTER TABLE recipeweave.recipe_step
ADD CONSTRAINT recipe_step_instruction_wire_length CHECK (CHAR_LENGTH(instruction) <= 5000)
```

## database/migrations/003_service_operations.sql:statement-285

```sql
ALTER TABLE recipeweave.recipe_ingredient
ADD CONSTRAINT recipe_ingredient_note_wire_length CHECK (CHAR_LENGTH(note) <= 500)
```

## database/migrations/003_service_operations.sql:statement-286

```sql
ALTER TABLE recipeweave.resource_type
ADD CONSTRAINT resource_type_name_wire_length CHECK (CHAR_LENGTH(name) <= 500)
```

## database/migrations/003_service_operations.sql:statement-287

```sql
ALTER TABLE recipeweave.axis_option
ADD CONSTRAINT axis_option_label_wire_length CHECK (CHAR_LENGTH(label) <= 500)
```

## database/migrations/004_backup_restore.sql:statement-8

```sql
ALTER TABLE recipeweave.backup_artifact ADD CONSTRAINT fk_backup_artifact_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE SET NULL ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/004_backup_restore.sql:statement-20

```sql
ALTER TABLE recipeweave.backup_restore_intent ADD CONSTRAINT fk_backup_restore_intent_user_id
FOREIGN KEY (user_id) REFERENCES recipeweave.app_user (id)
ON DELETE SET NULL ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/004_backup_restore.sql:statement-21

```sql
ALTER TABLE recipeweave.backup_restore_intent ADD CONSTRAINT fk_backup_restore_intent_artifact_id
FOREIGN KEY (artifact_id) REFERENCES recipeweave.backup_artifact (id)
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED
```

## database/migrations/004_backup_restore.sql:statement-25

```sql
CREATE FUNCTION recipeweave.guard_backup_artifact() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        IF NEW.user_id IS NULL THEN
            RAISE EXCEPTION 'バックアップの発行先を省略できません' USING ERRCODE = '23514';
        END IF;
        RETURN NEW;
    END IF;
    IF TG_OP = 'UPDATE' AND OLD.user_id IS NOT NULL AND NEW.user_id IS NULL
       AND (to_jsonb(NEW) - 'user_id') = (to_jsonb(OLD) - 'user_id')
       AND NOT EXISTS (SELECT 1 FROM recipeweave.app_user WHERE id = OLD.user_id) THEN
        RETURN NEW;
    END IF;
    RAISE EXCEPTION 'バックアップ発行記録は追記専用です' USING ERRCODE = '23514';
END;
$$
```

## database/migrations/004_backup_restore.sql:statement-26

```sql
CREATE FUNCTION recipeweave.guard_backup_restore_intent() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
DECLARE
    issued recipeweave.backup_artifact%ROWTYPE;
    workspace_revision bigint;
BEGIN
    IF TG_OP = 'DELETE' THEN
        RAISE EXCEPTION '復元確認記録は削除できません' USING ERRCODE = '23514';
    END IF;
    IF TG_OP = 'UPDATE' AND OLD.user_id IS NOT NULL AND NEW.user_id IS NULL
       AND (to_jsonb(NEW) - 'user_id') = (to_jsonb(OLD) - 'user_id')
       AND NOT EXISTS (SELECT 1 FROM recipeweave.app_user WHERE id = OLD.user_id) THEN
        RETURN NEW;
    END IF;
    IF NEW.user_id IS NULL THEN
        RAISE EXCEPTION '復元する本人を省略できません' USING ERRCODE = '23514';
    END IF;
    SELECT * INTO issued FROM recipeweave.backup_artifact WHERE id = NEW.artifact_id FOR KEY SHARE;
    IF NOT FOUND OR issued.user_id IS DISTINCT FROM NEW.user_id
       OR issued.body_sha256 <> NEW.body_sha256 THEN
        RAISE EXCEPTION 'バックアップの本人または本文が発行記録と一致しません' USING ERRCODE = '23514';
    END IF;
    SELECT revision INTO workspace_revision FROM recipeweave.workspace_revision
    WHERE user_id = NEW.user_id FOR UPDATE;
    IF NOT FOUND OR workspace_revision <> NEW.current_revision THEN
        RAISE EXCEPTION '確認後に現在データが変更されています。もう一度確認してください' USING ERRCODE = '23514';
    END IF;
    IF clock_timestamp() >= NEW.expires_at THEN
        RAISE EXCEPTION '復元確認の有効期限が切れています' USING ERRCODE = '23514';
    END IF;
    IF TG_OP = 'INSERT' THEN
        IF NEW.consumed_at IS NOT NULL THEN
            RAISE EXCEPTION '復元確認を使用済みとして発行できません' USING ERRCODE = '23514';
        END IF;
        RETURN NEW;
    END IF;
    IF OLD.consumed_at IS NOT NULL OR NEW.consumed_at IS NULL
       OR NEW.consumed_at > clock_timestamp()
       OR (to_jsonb(NEW) - 'consumed_at') <> (to_jsonb(OLD) - 'consumed_at') THEN
        RAISE EXCEPTION '復元確認は変更できず、一度だけ使用できます' USING ERRCODE = '23514';
    END IF;
    RETURN NEW;
END;
$$
```

## database/migrations/004_backup_restore.sql:statement-27

```sql
CREATE TRIGGER backup_artifact_append_only BEFORE INSERT OR UPDATE OR DELETE
ON recipeweave.backup_artifact
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_backup_artifact()
```

## database/migrations/004_backup_restore.sql:statement-28

```sql
CREATE TRIGGER backup_intent_single_use BEFORE INSERT OR UPDATE OR DELETE
ON recipeweave.backup_restore_intent
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_backup_restore_intent()
```

## database/migrations/004_backup_restore.sql:statement-29

```sql
ALTER TABLE recipeweave.backup_artifact ENABLE ROW LEVEL SECURITY
```

## database/migrations/004_backup_restore.sql:statement-30

```sql
ALTER TABLE recipeweave.backup_artifact FORCE ROW LEVEL SECURITY
```

## database/migrations/004_backup_restore.sql:statement-31

```sql
CREATE POLICY backup_evidence_owner ON recipeweave.backup_artifact
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
```

## database/migrations/004_backup_restore.sql:statement-32

```sql
ALTER TABLE recipeweave.backup_restore_intent ENABLE ROW LEVEL SECURITY
```

## database/migrations/004_backup_restore.sql:statement-33

```sql
ALTER TABLE recipeweave.backup_restore_intent FORCE ROW LEVEL SECURITY
```

## database/migrations/004_backup_restore.sql:statement-34

```sql
CREATE POLICY backup_evidence_owner ON recipeweave.backup_restore_intent
USING (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
) WITH CHECK (
    CURRENT_SETTING('recipeweave.role', TRUE) = 'admin'
    OR user_id = NULLIF(CURRENT_SETTING('recipeweave.user_id', TRUE), '')::UUID
)
```

## database/migrations/005_manual_duration.sql:statement-1

```sql
ALTER TABLE recipeweave.session_task
ADD COLUMN duration_source TEXT NOT NULL DEFAULT 'recipe_rule'
```

## database/migrations/005_manual_duration.sql:statement-3

```sql
ALTER TABLE recipeweave.session_task ADD COLUMN confirmed_duration_s INTEGER
```

## database/migrations/005_manual_duration.sql:statement-5

```sql
ALTER TABLE recipeweave.session_task ADD CONSTRAINT duration_source_values
CHECK (duration_source IN ('recipe_rule', 'user_estimate'))
```

## database/migrations/005_manual_duration.sql:statement-6

```sql
ALTER TABLE recipeweave.session_task ADD CONSTRAINT confirmed_duration_bounds
CHECK (confirmed_duration_s IS NULL OR confirmed_duration_s BETWEEN 1 AND 86400)
```

## database/migrations/005_manual_duration.sql:statement-7

```sql
ALTER TABLE recipeweave.session_task ADD CONSTRAINT duration_confirmation_matches_plan
CHECK (
    (duration_source = 'recipe_rule' AND confirmed_duration_s IS NULL)
    OR (
        duration_source = 'user_estimate' AND confirmed_duration_s IS NOT NULL
        AND planned_end_s - planned_start_s = confirmed_duration_s
    )
)
```

## database/migrations/005_manual_duration.sql:statement-8

```sql
CREATE FUNCTION recipeweave.guard_confirmed_task_plan() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.duration_source = 'user_estimate' AND NOT EXISTS (
        SELECT 1 FROM recipeweave.recipe_step step
        JOIN recipeweave.scaling_rule rule ON rule.id = step.scaling_rule_id
        WHERE step.id = NEW.step_id AND rule.mode = 'manual'
    ) THEN
        RAISE EXCEPTION '利用者の時間見積りは手動確認が必要な工程だけに指定できます' USING ERRCODE = '23514';
    END IF;
    IF TG_OP = 'UPDATE' THEN
        IF NEW.duration_source IS DISTINCT FROM OLD.duration_source
           OR NEW.confirmed_duration_s IS DISTINCT FROM OLD.confirmed_duration_s
           OR NEW.planned_start_s IS DISTINCT FROM OLD.planned_start_s
           OR NEW.planned_end_s IS DISTINCT FROM OLD.planned_end_s THEN
            RAISE EXCEPTION '確定した工程の時間根拠・見積り・計画時刻は変更できません' USING ERRCODE = '23514';
        END IF;
        IF OLD.duration_source = 'user_estimate' AND (
            NEW.step_id <> OLD.step_id OR NEW.menu_item_id <> OLD.menu_item_id
            OR NEW.session_id <> OLD.session_id OR NEW.batch_no <> OLD.batch_no
        ) THEN
            RAISE EXCEPTION '時間を確認した工程・献立・実行・バッチは変更できません' USING ERRCODE = '23514';
        END IF;
    END IF;
    RETURN NEW;
END;
$$
```

## database/migrations/005_manual_duration.sql:statement-9

```sql
CREATE TRIGGER confirmed_task_plan_immutable BEFORE INSERT OR UPDATE ON recipeweave.session_task
FOR EACH ROW EXECUTE FUNCTION recipeweave.guard_confirmed_task_plan()
```

## database/migrations/005_manual_duration.sql:statement-10

```sql
DO $$
DECLARE
    v_source_id uuid := '9decf898-19cd-5c03-b3e2-947d838c06bd';
    new_rule_id uuid := '9b2b5a4c-18db-5694-b175-96f9f2717e7c';
BEGIN
    IF NOT EXISTS (SELECT 1 FROM recipeweave.source_record WHERE id = v_source_id) THEN
        RETURN;
    END IF;
    INSERT INTO recipeweave.scaling_rule (
        id, name, mode, min_servings, max_servings, batch_capacity,
        round_mode, round_increment, source_id
    ) VALUES (
        new_rule_id,
        '人数変更時は利用者の時間見積りが必要（1〜1000は入力範囲・物理容量は別途確認）',
        'manual', 1, 1000, NULL, 'none', 0.01, v_source_id
    ) ON CONFLICT (id) DO NOTHING;
    IF NOT EXISTS (
        SELECT 1 FROM recipeweave.scaling_rule r
        WHERE r.id = new_rule_id AND r.mode = 'manual'
        AND r.name = '人数変更時は利用者の時間見積りが必要（1〜1000は入力範囲・物理容量は別途確認）'
        AND r.min_servings = 1 AND r.max_servings = 1000 AND r.batch_capacity IS NULL
        AND r.round_mode = 'none' AND r.round_increment = 0.01 AND r.source_id = v_source_id
    ) THEN
        RAISE EXCEPTION '移行先の時間規則IDに異なる定義があります' USING ERRCODE = '23514';
    END IF;
    UPDATE recipeweave.recipe_step step SET scaling_rule_id = new_rule_id
    FROM recipeweave.recipe_version version
    WHERE step.recipe_version_id = version.id AND version.status = 'draft'
    AND step.scaling_rule_id = 'aa59a90d-0a79-5f69-95a9-7857ffe94fad'
    AND version.id IN (
        'fcb0b2fa-f387-5a51-8bed-0b8f0a539e36', '0f3cb194-c9ef-5025-a738-227a3e712b0b',
        'bdcd3054-68c1-58f2-b544-bce1eda0b005', '5f21b805-9f20-508f-a7ca-a9cb7e4e1107',
        'f29a4fca-63ba-57be-8b93-a55e87132917', '519749b7-2259-56f0-ae91-840f24558453',
        '30509788-f24f-564e-8e32-70ced25efd69', '9a8ba1c3-7df7-5a7f-87dd-043538c39d37'
    );
END;
$$
```
